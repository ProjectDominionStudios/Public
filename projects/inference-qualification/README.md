# PDS Inference Qualification

**PDS Inference Qualification** is a Project Dominion Studios engineering initiative for evaluating large-language-model inference across hardware, inference engines, model architectures, and deployment configurations.

## Current Proof of Concept

The initial qualification platform is an enterprise GPU server named **Lurch**, equipped with a single **NVIDIA V100 32GB GPU (SM70)**.

The current investigation includes:

### Inference Engines

- vLLM
- llama.cpp

### Models

- Qwen2.5-14B-Instruct
- Qwen2.5-32B-Instruct
- Qwen3.6-35B-A3B / Hermes Genesis V7

### Measurements

Testing includes:

- Model compatibility
- Runtime compatibility
- Model loading behavior
- Concurrent requests
- Input throughput
- Output throughput
- Aggregate token throughput
- Request latency
- Context-window behavior
- GPU utilization
- VRAM utilization
- Power consumption
- Thermal behavior
- Failure conditions

## Why This Exists

Raw parameter count does not tell us whether a model is practical on a particular system.

Inference-engine implementation, model architecture, quantization, context configuration, workload characteristics, memory behavior, and hardware capabilities can dramatically change real-world performance.

The goal of this project is therefore not simply to ask:

> "Can this model run?"

It is to establish reproducible evidence for:

> **How well does this model and inference-engine combination perform on this hardware for a defined workload?**

## Publications

- [The Pascal Frontier — Whitepaper #1](the-pascal-frontier/wp1/): vLLM vs.
  llama.cpp on NVIDIA V100 / Volta / SM70, with public evidence and provenance.

## Documentation

The first complete proof of concept is now published. Additional whitepapers
and supporting evidence will be released after their own Founder review gates.

Planned publication includes:

- Hardware configuration
- Software stack
- Build methodology
- Inference-engine configuration
- Benchmark methodology
- Reproducible commands
- Compatibility findings
- Failure analysis
- Performance results
- Power and thermal measurements
- Graphs and comparisons
- Engineering observations and lessons learned

## Status

✅ **Whitepaper #1 published**

Additional benchmark work remains active and will be published as it is
reviewed and approved.

---

A **Project Dominion Studios** engineering project.
