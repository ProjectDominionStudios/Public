# PDS Volta vLLM Script Naming Standard

**Suite:** PDS Volta vLLM Compatibility & Benchmark Suite

## Stable executable names

- `pds-v100-vllm-build.sh` - deterministic build/patch/verification pipeline.
- `pds-v100-vllm-benchmark.sh` - unified smoke, standard, stress, concurrent, randomized, thermal/power, model-format and comparison harness.

Do not encode implementation revisions (`v7`, `v24`, etc.) in permanent filenames. Store version metadata inside the scripts and use Git tags/releases (`pds-v100-vllm-suite-v1.0.0`).

## Suggested metadata

```bash
SCRIPT_NAME="pds-v100-vllm-benchmark"
SCRIPT_VERSION="1.0.0"
PDS_SUITE_VERSION="1.0.0"
```

Support `--version` and record the script version into every run summary.
