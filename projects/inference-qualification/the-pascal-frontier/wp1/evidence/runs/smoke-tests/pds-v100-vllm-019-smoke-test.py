from __future__ import annotations

import multiprocessing as mp
import sys
import time
from pathlib import Path

import torch
import vllm
from vllm import LLM, SamplingParams


def main() -> None:
    model = sys.argv[1]
    max_model_len = int(sys.argv[2])
    max_tokens = int(sys.argv[3])
    gpu_memory_utilization = float(sys.argv[4])

    print("=" * 80)
    print("PDS V100 vLLM smoke test")
    print("=" * 80)
    print(f"Python: {sys.version.split()[0]}")
    print(f"PyTorch: {torch.__version__}")
    print(f"PyTorch CUDA: {torch.version.cuda}")
    print(f"vLLM: {vllm.__version__}")
    print(f"Model: {model}")

    assert torch.cuda.is_available(), "CUDA is not available to PyTorch"

    gpu_name = torch.cuda.get_device_name(0)
    gpu_capability = torch.cuda.get_device_capability(0)
    gpu_memory_gib = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)

    print(f"GPU: {gpu_name}")
    print(f"GPU capability: {gpu_capability}")
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

    print("PASS: environment, CUDA, SM70, and binary-profile checks")

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
    print(f"Engine initialization: {init_seconds:.2f} seconds")

    start_generate = time.perf_counter()
    outputs = llm.generate(prompts, sampling)
    generate_seconds = time.perf_counter() - start_generate

    assert len(outputs) == len(prompts), (
        f"Expected {len(prompts)} outputs, received {len(outputs)}"
    )

    for index, output in enumerate(outputs, start=1):
        generated = output.outputs[0].text
        assert generated.strip(), f"Prompt {index} returned empty text"
        print()
        print(f"Prompt {index}:")
        print(output.prompt)
        print(f"Generated {index}:")
        print(generated)

    print()
    print(f"Generation time: {generate_seconds:.2f} seconds")
    print("PASS: model loaded and generated non-empty output for all prompts")
    print("SMOKE_TEST_RESULT=PASS")

    # Ensure the engine object is released before interpreter shutdown.
    del llm


if __name__ == "__main__":
    mp.freeze_support()
    main()

