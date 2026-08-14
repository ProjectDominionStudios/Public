from __future__ import annotations
import asyncio, json, random, sys, time, urllib.request

base=sys.argv[1]
users=int(sys.argv[2])
requests_per_user=int(sys.argv[3])
max_tokens=int(sys.argv[4])
think_ms=int(sys.argv[5])
model=sys.argv[6]
random_stress=bool(int(sys.argv[7]))
seed=int(sys.argv[8])
input_min=int(sys.argv[9])
input_max=int(sys.argv[10])
output_min=int(sys.argv[11])
output_max=int(sys.argv[12])

latencies=[]
failures=0
output_tokens=0
input_tokens_est=0
lock=asyncio.Lock()

# Deterministic per-user RNG streams make the random workload reproducible.
def request_shape(uid, rid):
    rng=random.Random(seed + uid*100000 + rid)
    if not random_stress:
        return 24, max_tokens, think_ms
    input_target=rng.randint(input_min,input_max)
    output_target=rng.randint(output_min,output_max)
    think_target=rng.randint(0, max(think_ms,250))
    return input_target, output_target, think_target

def make_prompt(uid, rid, input_target):
    # Approximate target token count with repeated short words. Exact tokenizer
    # counts are captured by the server response usage when available.
    core=f"Concurrent randomized inference test user {uid} request {rid}. "
    filler="reliable AI infrastructure practical business workflow data automation "
    words=[]
    approx_words=max(1,int(input_target*0.75))
    while len(words)<approx_words:
        words.extend(filler.split())
    return core+" ".join(words[:approx_words])

def request_once(uid,rid):
    input_target, output_target, _ = request_shape(uid,rid)
    prompt=make_prompt(uid,rid,input_target)
    payload=json.dumps({
        "model":model,
        "prompt":prompt,
        "max_tokens":output_target,
        "temperature":0.0,
    }).encode()
    req=urllib.request.Request(
        base+"/v1/completions", data=payload,
        headers={"Content-Type":"application/json"}, method="POST")
    t0=time.perf_counter()
    with urllib.request.urlopen(req,timeout=180) as resp:
        body=json.loads(resp.read())
    dt=time.perf_counter()-t0
    text=((body.get("choices") or [{}])[0].get("text") or "").strip()
    if not text:
        raise RuntimeError("empty completion")
    usage=body.get("usage") or {}
    out_tok=int(usage.get("completion_tokens") or 0)
    in_tok=int(usage.get("prompt_tokens") or input_target)
    return dt,in_tok,out_tok

async def worker(uid):
    global failures, output_tokens, input_tokens_est
    for rid in range(1,requests_per_user+1):
        _,_,think_target=request_shape(uid,rid)
        try:
            dt,in_tok,out_tok=await asyncio.to_thread(request_once,uid,rid)
            async with lock:
                latencies.append(dt)
                input_tokens_est+=in_tok
                output_tokens+=out_tok
        except Exception as e:
            async with lock:
                failures+=1
            print(f"CLIENT_ERROR:user={uid}|request={rid}|{type(e).__name__}:{e}",flush=True)
        if think_target:
            await asyncio.sleep(think_target/1000)

def pct(vals,q):
    if not vals:
        return 0.0
    vals=sorted(vals)
    pos=(len(vals)-1)*q
    lo=int(pos); hi=min(lo+1,len(vals)-1); f=pos-lo
    return vals[lo]*(1-f)+vals[hi]*f

async def main():
    t0=time.perf_counter()
    await asyncio.gather(*(worker(i) for i in range(1,users+1)))
    elapsed=time.perf_counter()-t0
    completed=len(latencies)
    total=users*requests_per_user
    print(f"CONCURRENT_RESULT:total={total}|completed={completed}|failures={failures}|seconds={elapsed:.4f}",flush=True)
    print(f"Concurrent requests/sec: {(completed/elapsed if elapsed else 0):.2f}",flush=True)
    print(f"Concurrent input tokens/sec: {(input_tokens_est/elapsed if elapsed else 0):.2f}",flush=True)
    print(f"Concurrent output tokens/sec: {(output_tokens/elapsed if elapsed else 0):.2f}",flush=True)
    print(f"Concurrent total tokens/sec: {((input_tokens_est+output_tokens)/elapsed if elapsed else 0):.2f}",flush=True)
    print(f"Latency p50: {pct(latencies,.50):.4f} seconds",flush=True)
    print(f"Latency p95: {pct(latencies,.95):.4f} seconds",flush=True)
    print(f"Latency p99: {pct(latencies,.99):.4f} seconds",flush=True)
    print(f"Concurrent input tokens: {input_tokens_est}",flush=True)
    print(f"Concurrent output tokens: {output_tokens}",flush=True)
    print("CONCURRENT_TEST_RESULT="+("PASS" if failures==0 and completed==total else "FAIL"),flush=True)
    raise SystemExit(0 if failures==0 and completed==total else 1)

if __name__=="__main__":
    asyncio.run(main())

