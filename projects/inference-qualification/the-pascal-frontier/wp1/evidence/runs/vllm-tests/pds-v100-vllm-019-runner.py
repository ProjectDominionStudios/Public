from __future__ import annotations

import sys
import time
from pathlib import Path

import torch
import vllm
from vllm import LLM, SamplingParams


def main():
    model = sys.argv[1]
    level = sys.argv[2]
    max_model_len = int(sys.argv[3])
    max_tokens = int(sys.argv[4])
    gpu_memory_utilization = float(sys.argv[5])
    prompt_count = int(sys.argv[6])
    rounds = int(sys.argv[7])

    print("=" * 80)
    print(f"PDS V100 vLLM {level} test")
    print("=" * 80)
    print(f"Python: {sys.version.split()[0]}", flush=True)
    print(f"PyTorch: {torch.__version__}", flush=True)
    print(f"PyTorch CUDA: {torch.version.cuda}", flush=True)
    print(f"vLLM: {vllm.__version__}", flush=True)
    print(f"Model: {model}", flush=True)
    print(
        f"Workload: {prompt_count} prompts x {max_tokens} max tokens x {rounds} rounds",
        flush=True,
    )

    assert torch.cuda.is_available(), "CUDA is not available to PyTorch"

    gpu_name = torch.cuda.get_device_name(0)
    gpu_capability = torch.cuda.get_device_capability(0)
    gpu_memory_gib = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)

    print(f"GPU: {gpu_name}", flush=True)
    print(f"GPU capability: {gpu_capability}", flush=True)
    print(f"GPU memory: {gpu_memory_gib:.2f} GiB", flush=True)

    assert gpu_capability == (7, 0), (
        f"Expected Tesla V100 / SM70 capability (7, 0), got {gpu_capability}"
    )

    root = Path(vllm.__file__).resolve().parent
    forbidden = (
        "_vllm_fa2_C",
        "_vllm_fa3_C",
        "_flashmla_C",
        "_flashmla_extension_C",
        "_deep_gemm_C",
    )
    unexpected = [
        str(path)
        for path in root.rglob("*.so")
        if any(name in path.name for name in forbidden)
    ]
    assert not unexpected, (
        "Unsupported bundled CUDA binaries were found:\n" + "\n".join(unexpected)
    )

    print("PASS: environment, CUDA, SM70, and binary-profile checks", flush=True)

    seeds = [
        "Project Dominion Studios is building",
        "A Tesla V100 is useful for",
        "Human-readable and machine-readable documentation should",
        "Open-source infrastructure projects benefit from",
        "A reproducible compatibility test should",
        "GPU engineering requires careful validation because",
        "A good technical runbook should include",
        "Reliable AI infrastructure depends on",
    ]
    prompts = [f"{seeds[i % len(seeds)]} [case {i + 1}]" for i in range(prompt_count)]

    sampling = SamplingParams(
        temperature=0.0,
        max_tokens=max_tokens,
    )

    start_init = time.perf_counter()
    llm = LLM(
        model=model,
        dtype="float16",
        attention_backend="TRITON_ATTN",
        enforce_eager=True,
        max_model_len=max_model_len,
        gpu_memory_utilization=gpu_memory_utilization,
    )
    init_seconds = time.perf_counter() - start_init
    print(f"Engine initialization: {init_seconds:.2f} seconds", flush=True)

    total_generation_seconds = 0.0
    total_output_tokens = 0
    total_requests = 0

    for round_index in range(1, rounds + 1):
        print(f"ROUND_START:{round_index}/{rounds}", flush=True)
        start_generate = time.perf_counter()
        outputs = llm.generate(prompts, sampling)
        round_seconds = time.perf_counter() - start_generate

        assert len(outputs) == len(prompts), (
            f"Expected {len(prompts)} outputs, received {len(outputs)}"
        )

        round_tokens = 0
        for index, output in enumerate(outputs, start=1):
            generated = output.outputs[0].text
            assert generated.strip(), (
                f"Round {round_index}, prompt {index} returned empty text"
            )
            token_ids = getattr(output.outputs[0], "token_ids", None) or []
            round_tokens += len(token_ids)

        total_generation_seconds += round_seconds
        total_output_tokens += round_tokens
        total_requests += len(outputs)

        round_tps = round_tokens / round_seconds if round_seconds > 0 else 0.0
        print(
            f"ROUND_RESULT:{round_index}/{rounds}|requests={len(outputs)}|"
            f"output_tokens={round_tokens}|seconds={round_seconds:.4f}|"
            f"output_tokens_per_sec={round_tps:.2f}",
            flush=True,
        )

    requests_per_second = (
        total_requests / total_generation_seconds if total_generation_seconds > 0 else 0.0
    )
    output_tokens_per_second = (
        total_output_tokens / total_generation_seconds
        if total_generation_seconds > 0
        else 0.0
    )

    print(f"Generation time: {total_generation_seconds:.4f} seconds", flush=True)
    print(f"Requests: {total_requests}", flush=True)
    print(f"Output tokens: {total_output_tokens}", flush=True)
    print(f"Requests/sec: {requests_per_second:.2f}", flush=True)
    print(f"Output tokens/sec: {output_tokens_per_second:.2f}", flush=True)
    print("PASS: model generated non-empty output for all requests", flush=True)
    print("SMOKE_TEST_RESULT=PASS", flush=True)


if __name__ == "__main__":
    main()

