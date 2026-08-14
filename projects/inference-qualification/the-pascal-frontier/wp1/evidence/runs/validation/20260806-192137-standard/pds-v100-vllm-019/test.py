from __future__ import annotations
import gc, json, multiprocessing as mp, sys, time
from pathlib import Path
import torch
import torch.distributed as dist
import vllm
from vllm import LLM, SamplingParams

def cleanup(llm):
    for obj in (llm, getattr(llm, "llm_engine", None), getattr(getattr(llm, "llm_engine", None), "engine_core", None)):
        if obj is not None:
            fn = getattr(obj, "shutdown", None)
            if callable(fn):
                try: fn()
                except Exception as e: print("WARNING shutdown:", e)
    if dist.is_available() and dist.is_initialized():
        try:
            dist.destroy_process_group()
            print("PASS: parent process group destroyed")
        except Exception as e:
            print("WARNING destroy_process_group:", e)
    del llm
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def main():
    model, level, out_json, prompt_count, max_tokens, rounds, max_model_len, gpu_mem = sys.argv[1:9]
    prompt_count, max_tokens, rounds, max_model_len = map(int, (prompt_count, max_tokens, rounds, max_model_len))
    gpu_mem = float(gpu_mem)
    r = dict(status="FAIL", level=level, model=model, python=sys.version.split()[0], pytorch=torch.__version__,
             pytorch_cuda=torch.version.cuda, vllm=vllm.__version__, attention_backend="TRITON_ATTN",
             requests_total=0, input_tokens_total=0, output_tokens_total=0, generation_seconds_total=0.0)
    llm = None
    try:
        assert torch.cuda.is_available()
        cap = torch.cuda.get_device_capability(0)
        assert cap == (7,0), f"Expected SM70, got {cap}"
        r["gpu_name"] = torch.cuda.get_device_name(0)
        r["gpu_capability"] = list(cap)

        root = Path(vllm.__file__).resolve().parent
        bad = ("_vllm_fa2_C","_vllm_fa3_C","_flashmla_C","_flashmla_extension_C","_deep_gemm_C")
        found = [str(p) for p in root.rglob("*.so") if any(x in p.name for x in bad)]
        assert not found, "Unsupported binaries: " + ", ".join(found)

        seeds = [
            "Project Dominion Studios is building",
            "A Tesla V100 is useful for",
            "Human-readable and machine-readable documentation should",
            "Open-source infrastructure projects benefit from",
            "A good regression test should verify",
            "GPU compatibility engineering requires",
            "The purpose of reproducible builds is",
            "A technical runbook should include",
        ]
        prompts = [f"{seeds[i % len(seeds)]} [case {i+1}]" for i in range(prompt_count)]
        params = SamplingParams(temperature=0.0, max_tokens=max_tokens)

        t0 = time.perf_counter()
        llm = LLM(model=model, dtype="float16", attention_backend="TRITON_ATTN",
                  enforce_eager=True, max_model_len=max_model_len,
                  gpu_memory_utilization=gpu_mem)
        r["engine_init_seconds"] = round(time.perf_counter()-t0, 6)

        durations=[]
        for n in range(rounds):
            t0=time.perf_counter()
            outputs=llm.generate(prompts, params)
            dt=time.perf_counter()-t0
            durations.append(dt)
            assert len(outputs)==len(prompts)
            out_tok=0
            in_tok=0
            for o in outputs:
                assert o.outputs[0].text.strip()
                in_tok += len(getattr(o,"prompt_token_ids",None) or [])
                out_tok += len(getattr(o.outputs[0],"token_ids",None) or [])
            r["requests_total"] += len(outputs)
            r["input_tokens_total"] += in_tok
            r["output_tokens_total"] += out_tok
            r["generation_seconds_total"] += dt
            print(f"ROUND {n+1}/{rounds}: requests={len(outputs)} output_tokens={out_tok} seconds={dt:.3f}")

        r["generation_seconds_total"]=round(r["generation_seconds_total"],6)
        r["requests_per_second"]=round(r["requests_total"]/r["generation_seconds_total"],4)
        r["output_tokens_per_second"]=round(r["output_tokens_total"]/r["generation_seconds_total"],4)
        r["first_round_seconds"]=round(durations[0],6)
        r["last_round_seconds"]=round(durations[-1],6)
        r["status"]="PASS"
        print("VALIDATION_RESULT=PASS")
        print(json.dumps(r, indent=2))
        return 0
    except Exception as e:
        r["error"]=f"{type(e).__name__}: {e}"
        print("VALIDATION_RESULT=FAIL", r["error"], file=sys.stderr)
        return 1
    finally:
        if llm is not None:
            cleanup(llm)
        Path(out_json).write_text(json.dumps(r, indent=2)+"\n")

if __name__ == "__main__":
    mp.freeze_support()
    raise SystemExit(main())
