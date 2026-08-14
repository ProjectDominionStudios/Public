# PDS V100 vLLM Validation Comparison

| Version | vLLM build | Level | Result | Init s | Gen s | Requests | Out tok/s | Avg GPU % | Peak VRAM MiB | Peak W | Peak C | GPU release |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0.19.0 | 0.19.1.dev0+g2a69949bd.d20260807 | standard | PASS | 11.762438 | 1.841096 | 48 | 1668.5713 | 6.333 | 26334.0 | 80.55 | 34.0 | PASS |
| 0.21.0 | 0.21.1.dev0+gad7125a43.d20260807 | standard | PASS | 12.511725 | 1.95445 | 48 | 1571.7977 | 5.875 | 26334.0 | 52.32 | 35.0 | PASS |
