# M21 Prerequisites

Required on both nodes: Python 3, OpenSSL, Git, systemd userspace and the M20 source baseline. Useful live-audit tools include `mokutil`, `fwupdmgr`, `aa-status`, `getenforce`, `capsh`, `setpriv`, `systemd-analyze`, and `tpm2-tools`; absence is captured as evidence and does not get silently converted to success.

Node2 Jetson validation may additionally use NVIDIA `nv_fuse_read.sh` when installed/authorized. M21 never invokes fuse-burn or flash commands.
