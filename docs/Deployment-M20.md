# M20 Deployment

Node1 runs `deploy/m20/one_shot_node1.sh <M19-summary> [output]`, signs the final-freeze evidence, and packages verifier-only material. Node2 receives only the verifier archive and runs `deploy/m20/one_shot_node2.sh`. The scripts deploy configuration/evidence only; they do not flash firmware, update the host OS, or contact external services.
