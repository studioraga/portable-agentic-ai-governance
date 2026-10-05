# Deployment — M26

## Node1

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
./deploy/m26/one_shot_node1.sh
```

Transfer only `var/m26-verifier.tar.gz` and its checksum to Node2.

## Node2

Apply the same M26 source uncommitted, create the Python environment, validate the archive checksum, then run:

```bash
./deploy/m26/one_shot_node2.sh m26-verifier.tar.gz /tmp/m26-node1
```

Production SOC and backup integrations are operator-controlled and are not silently installed or reconfigured by M26 validation.
