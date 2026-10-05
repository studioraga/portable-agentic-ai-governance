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

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.
