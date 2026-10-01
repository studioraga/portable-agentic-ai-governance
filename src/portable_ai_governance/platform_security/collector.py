from __future__ import annotations
import json,os,platform,shutil,socket,subprocess
from pathlib import Path

def _run(cmd,timeout=5):
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,check=False)
        return {'rc':p.returncode,'out':p.stdout.strip(),'err':p.stderr.strip()}
    except Exception as e:return {'rc':127,'out':'','err':str(e)}

def _sysctl(name):
    p=Path('/proc/sys')/Path(name.replace('.','/'))
    try:return int(p.read_text().strip())
    except Exception:return None

def _osrel():
    d={}
    try:
        for line in Path('/etc/os-release').read_text().splitlines():
            if '=' in line:
                k,v=line.split('=',1);d[k.lower()]=v.strip().strip('"')
    except Exception:pass
    return {'id':d.get('id','unknown'),'version_id':d.get('version_id','unknown'),'pretty_name':d.get('pretty_name','unknown')}

def _secure_boot():
    if shutil.which('mokutil'):
        r=_run(['mokutil','--sb-state']);o=(r['out']+' '+r['err']).lower()
        if 'enabled' in o:return 'enabled'
        if 'disabled' in o:return 'disabled'
    efi=Path('/sys/firmware/efi/efivars')
    if efi.exists():
        for p in efi.glob('SecureBoot-*'):
            try:return 'enabled' if p.read_bytes()[-1]==1 else 'disabled'
            except Exception:pass
    return 'unknown'

def _lockdown():
    lockdown = Path(
        '/sys/kernel/security/lockdown'
    )

    if lockdown.exists():
        try:
            text = lockdown.read_text(
                errors='replace'
            ).strip()

            for state in (
                'integrity',
                'confidentiality',
                'none',
            ):
                if f'[{state}]' in text:
                    return state

            return text or 'unknown'

        except Exception:
            return 'unknown'

    # Jetson kernels may not install /boot/config-*.
    # Fall back to IKCONFIG when /proc/config.gz exists.
    config_gz = Path('/proc/config.gz')

    if config_gz.exists():
        try:
            import gzip

            with gzip.open(
                config_gz,
                'rt',
                errors='replace',
            ) as f:
                for line in f:
                    line = line.strip()

                    if (
                        line ==
                        '# CONFIG_SECURITY_LOCKDOWN_LSM is not set'
                    ):
                        return 'unsupported-by-kernel-config'

                    if (
                        line ==
                        'CONFIG_SECURITY_LOCKDOWN_LSM=y'
                    ):
                        return (
                            'supported-interface-unavailable'
                        )

        except Exception:
            pass

    return 'unknown'

def _apparmor():
    userspace_available = shutil.which('aa-status') is not None

    interface = Path(
        '/sys/module/apparmor/parameters/enabled'
    )

    kernel_interface_present = interface.exists()

    kernel_enabled = False
    if kernel_interface_present:
        try:
            kernel_enabled = (
                interface.read_text(
                    errors='replace'
                ).strip().upper() == 'Y'
            )
        except Exception:
            kernel_enabled = False

    active_lsms = []
    try:
        text = Path(
            '/sys/kernel/security/lsm'
        ).read_text(errors='replace')

        active_lsms = [
            x.strip()
            for x in text.split(',')
            if x.strip()
        ]
    except Exception:
        pass

    active_lsm = 'apparmor' in active_lsms

    enforcing = False
    detail = 'not-detected'

    if userspace_available:
        r = _run(['aa-status'])

        detail = (
            r['out']
            or r['err']
            or ''
        )[:2000]

        if (
            r['rc'] == 0
            and active_lsm
            and kernel_enabled
        ):
            lower = detail.lower()

            enforcing = (
                'profiles are in enforce mode' in lower
                and
                '0 profiles are in enforce mode' not in lower
            )

    available = (
        kernel_interface_present
        and kernel_enabled
        and active_lsm
    )

    if userspace_available and not available:
        detail = (
            'AppArmor userspace installed; '
            'kernel AppArmor LSM unavailable/inactive. '
            + detail
        )[:2000]

    return {
        'userspace_available': userspace_available,
        'kernel_interface_present': kernel_interface_present,
        'kernel_enabled': kernel_enabled,
        'active_lsm': active_lsm,
        'available': available,
        'enforcing': enforcing,
        'detail': detail,
    }

def _selinux():
    selinux_fs = Path('/sys/fs/selinux')
    enforce_file = selinux_fs / 'enforce'

    kernel_interface_present = enforce_file.exists()

    active_lsms = []
    try:
        text = Path(
            '/sys/kernel/security/lsm'
        ).read_text(errors='replace')

        active_lsms = [
            x.strip()
            for x in text.split(',')
            if x.strip()
        ]
    except Exception:
        pass

    active_lsm = 'selinux' in active_lsms

    userspace_available = (
        shutil.which('getenforce') is not None
    )

    mode = 'unknown'

    if kernel_interface_present:
        try:
            raw = enforce_file.read_text(
                errors='replace'
            ).strip()

            if raw == '1':
                mode = 'enforcing'
            elif raw == '0':
                mode = 'permissive'
            else:
                mode = f'unknown:{raw}'

        except Exception:
            mode = 'unknown'

    elif not active_lsm:
        mode = 'disabled'

    elif userspace_available:
        r = _run(['getenforce'])
        mode = (
            r['out']
            or r['err']
            or 'unknown'
        ).strip().lower()

    available = (
        kernel_interface_present
        and active_lsm
    )

    return {
        'userspace_available': userspace_available,
        'kernel_interface_present':
            kernel_interface_present,
        'active_lsm': active_lsm,
        'available': available,
        'enforcing': mode.lower() == 'enforcing',
        'mode': mode,
    }

def _tpm():
    dev_tpm0 = Path('/dev/tpm0').exists()
    dev_tpmrm0 = Path('/dev/tpmrm0').exists()
    device_present = dev_tpm0 or dev_tpmrm0

    cap_ok = False
    cap_excerpt = ''
    if device_present and shutil.which('tpm2_getcap'):
        r = _run(['tpm2_getcap', 'properties-fixed'])
        cap_ok = r['rc'] == 0 and bool(r['out'])
        cap_excerpt = (r['out'] or r['err'])[:2000]

    pcr = None
    if device_present and shutil.which('tpm2_pcrread'):
        r = _run(['tpm2_pcrread', 'sha256:0,2,4,7'])
        if r['rc'] == 0 and r['out']:
            pcr = r['out']

    return {
        'available': device_present,
        'device_present': device_present,
        'usable': cap_ok,
        'pcrs_available': bool(pcr),
        'pcr_excerpt': (pcr or '')[:2000],
        'capability_excerpt': cap_excerpt,
    }

def _firmware_info():
    def read(p):
        try:return Path(p).read_text(errors='replace').strip()
        except Exception:return 'unknown'
    bmc=Path('/dev/ipmi0').exists() or Path('/dev/ipmi/0').exists()
    jetson=Path('/etc/nv_tegra_release').exists()
    fuse='unavailable'
    if jetson and shutil.which('nv_fuse_read.sh'):
        r=_run(['sudo','-n','nv_fuse_read.sh','-l']);fuse='available' if r['rc']==0 else 'present-needs-privilege'
    return {'bios_vendor':read('/sys/class/dmi/id/bios_vendor'),'bios_version':read('/sys/class/dmi/id/bios_version'),'bmc_present':bmc,'jetson':jetson,'jetson_fuse_reader':fuse,'fwupdmgr_available':shutil.which('fwupdmgr') is not None}

def collect_profile(role,node_id=None):
    arch=platform.machine();jetson=Path('/etc/nv_tegra_release').exists()
    chain=['BootROM/fuses','MB1','MB2','UEFI','kernel/DTB/initrd','rootfs','systemd-services'] if jetson else ['hardware-root/firmware','UEFI','shim/grub','kernel','initramfs','rootfs','systemd-services']
    return {'schema_version':'1.0','milestone':'M21','capture_mode':'LIVE','node_id':node_id or socket.gethostname(),'role':role,'hostname':socket.gethostname(),'architecture':arch,'os':_osrel(),'kernel_release':platform.release(),'boot':{'uefi':Path('/sys/firmware/efi').exists(),'secure_boot':_secure_boot(),'kernel_lockdown':_lockdown(),'chain':chain},'firmware':_firmware_info(),'debug':{'kernel.yama.ptrace_scope':_sysctl('kernel.yama.ptrace_scope'),'kernel.kptr_restrict':_sysctl('kernel.kptr_restrict'),'kernel.dmesg_restrict':_sysctl('kernel.dmesg_restrict'),'kernel.perf_event_paranoid':_sysctl('kernel.perf_event_paranoid'),'kernel.sysrq':_sysctl('kernel.sysrq')},'linux_privilege':{'capsh_available':shutil.which('capsh') is not None,'setpriv_available':shutil.which('setpriv') is not None},'service_isolation':{'systemd_analyze_available':shutil.which('systemd-analyze') is not None},'mac':{'apparmor':_apparmor(),'selinux':_selinux()},'root_of_trust':{'tpm':_tpm(),'dice':{'hardware_available':False,'demo_available':True},'platform_hardware_root':bool(jetson or Path('/sys/firmware/efi').exists())}}
