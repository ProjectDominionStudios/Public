from __future__ import annotations

import sys
import time
from pathlib import Path

import torch
import vllm
from vllm import LLM, SamplingParams


def main():
    model = sys.argv[1]
    max_model_len = int(sys.argv[2])
    max_tokens = int(sys.argv[3])
    gpu_memory_utilization = float(sys.argv[4])

    print("=" * 80)
    print("PDS V100 vLLM smoke test")
    print("=" * 80)
    print(f"Python: {sys.version.split()[0]}", flush=True)
    print(f"PyTorch: {torch.__version__}", flush=True)
    print(f"PDS_EVIDENCE|PyTorch|{torch.__version__}")
    print(f"PyTorch CUDA: {torch.version.cuda}", flush=True)
    print(f"PDS_EVIDENCE|CUDA|{torch.version.cuda}")
    print(f"vLLM: {vllm.__version__}", flush=True)
    print(f"PDS_EVIDENCE|vLLM|{vllm.__version__}")
    print(f"Model: {model}")

    assert torch.cuda.is_available(), "CUDA is not available to PyTorch"

    gpu_name = torch.cuda.get_device_name(0)
    gpu_capability = torch.cuda.get_device_capability(0)
    gpu_memory_gib = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)

    print(f"GPU: {gpu_name}", flush=True)
    print(f"GPU capability: {gpu_capability}", flush=True)
    print(f"GPU memory: {gpu_memory_gib:.2f} GiB")

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

    prompts = [
        "Project Dominion Studios is building",
        "A Tesla V100 is useful for",
        "Human-readable and machine-readable documentation should",
    ]

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

    start_generate = time.perf_counter()
    outputs = llm.generate(prompts, sampling)
    generate_seconds = time.perf_counter() - start_generate

    assert len(outputs) == len(prompts), (
        f"Expected {len(prompts)} outputs, received {len(outputs)}"
    )

    total_output_tokens = 0
    for index, output in enumerate(outputs, start=1):
        generated = output.outputs[0].text
        assert generated.strip(), f"Prompt {index} returned empty text"
        token_ids = getattr(output.outputs[0], "token_ids", None) or []
        total_output_tokens += len(token_ids)
        print()
        print(f"Prompt {index}:")
        print(output.prompt)
        print(f"Generated {index}:")
        print(generated)

    requests_per_second = len(outputs) / generate_seconds if generate_seconds > 0 else 0.0
    output_tokens_per_second = (
        total_output_tokens / generate_seconds if generate_seconds > 0 else 0.0
    )

    print()
    print(f"Generation time: {generate_seconds:.4f} seconds", flush=True)
    print(f"Output tokens: {total_output_tokens}", flush=True)
    print(f"Requests/sec: {requests_per_second:.2f}", flush=True)
    print(f"Output tokens/sec: {output_tokens_per_second:.2f}", flush=True)
    print("PASS: model loaded and generated non-empty output for all prompts", flush=True)
    print("SMOKE_TEST_RESULT=PASS", flush=True)

if __name__ == "__main__":
    main()
