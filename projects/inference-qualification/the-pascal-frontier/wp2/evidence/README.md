# WP2 public evidence

Sanitized records supporting The Pascal Frontier Whitepaper #2.

| Source | Record |
|---|---|
| [S04](runs/S04/) | 35B 1 user × 2 requests: PASS |
| [S05](runs/S05/) | 35B 2 users × 5 requests: CUDA/Triton OOM |
| [S06](runs/S06/) | 35B 4 users × 5 requests: failure |
| [S07](runs/S07/) | Selected 14B run: 80/80 completed |
| [S08](runs/S08/) | Selected 32B run: 80/80 completed |
| [S09](runs/S09/) | Early 14B GPTQ startup failure |
| [S15](runs/S15/) | Verified four-commit parent chain and nine-file patch diff |

[Claim ledger](claim-ledger.csv) · [Public file manifest](source-manifest.csv) · [Original integrity audit](original-integrity-audit.json) · [Telemetry calculations](telemetry-recalculation.json)

The three selected 35B runs and successful 14B/32B runs each pass all 13 original archived checksums. The early GPTQ failure has one server.log checksum mismatch; its other 10 checks pass. The exception is preserved, not repaired.

Personal home-directory names and ephemeral loopback ports are normalized. Original sha256sum.txt files apply to original archived bytes; use the public manifest for these text derivatives. No environment dumps, credentials, private governance documents, or model weights are included. This package supports historical observations, not an independent rerun or an upstream-merge claim.

The two-request 35B pass is not a sustained capacity test. Power averages span startup through cleanup; they are not generation-only efficiency measurements.

## Series evidence

- [WP1 evidence](../../wp1/evidence/)
- [WP2 evidence](./)
