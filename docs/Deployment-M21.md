# M21 Deployment

1. Apply the same uncommitted M21 source to Node1 and Node2.
2. Run focused and CI validation on both nodes.
3. Node2 captures a live platform profile and sends only that JSON to Node1.
4. Node1 captures its own live profile, builds/signs the M21 material and packages verifier-only material.
5. Node2 verifies the signed bundle independently.
6. Run tamper/private-key negative tests before commit.

No firmware is flashed and no irreversible platform configuration is changed by these scripts.
