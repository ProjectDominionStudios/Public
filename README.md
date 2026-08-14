# Project Dominion Studios — Public

Welcome to the public engineering repository for **Project Dominion Studios**.

This repository contains public projects, technical research, tools, demonstrations, benchmark evidence, experiments, and published engineering work from Project Dominion Studios.

## Projects

### PDS Inference Qualification

A reproducible investigation of modern large-language-model inference across models, inference engines, and hardware platforms.

Current work includes:

- NVIDIA V100 32GB (SM70) enterprise GPU hardware
- vLLM
- llama.cpp
- GGUF and quantized model formats
- Dense transformer models
- Mixture-of-Experts (MoE) architectures
- Concurrent inference workloads
- Context-window testing
- Throughput and latency measurement
- GPU utilization
- Power consumption
- Thermal behavior
- Runtime compatibility and failure analysis

Initial model testing includes:

- Qwen2.5-14B-Instruct
- Qwen2.5-32B-Instruct
- Qwen3.6-35B-A3B / Hermes Genesis V7

The first documented proof of concept, benchmark methodology, reproducible
configurations, results, build notes, failures, and lessons learned are now
published as **The Pascal Frontier — Whitepaper #1**.

See:

[`projects/inference-qualification`](projects/inference-qualification)

Direct publication: [`The Pascal Frontier — Whitepaper #1`](projects/inference-qualification/the-pascal-frontier/wp1/)

## About Project Dominion Studios

**Project Dominion Studios** is a technology and innovation studio focused on AI, automation, software engineering, cloud technologies, developer tools, and interactive experiences.

This repository represents work intentionally approved for public release.

## Status

✅ **Whitepaper #1 published; active development continues**

---

**Build. Measure. Document. Improve.**
