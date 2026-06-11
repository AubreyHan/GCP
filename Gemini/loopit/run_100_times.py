import os
import time
from collections import Counter

# Import variables from loopit (safe to import now)
from loopit import client, config, user_prompt

NUM_RUNS = 100
print(f"Running gemini-3.5-flash for {NUM_RUNS} times with loopit config...")

stop_reasons = Counter()
mfc_count = 0
success_runs = 0

i = 1
while i <= NUM_RUNS:
    print(f"--- Run {i}/{NUM_RUNS} ---", end=" ", flush=True)
    try:
        response_stream = client.models.generate_content_stream(
            model="gemini-3.5-flash",
            contents=user_prompt,
            config=config
        )
        
        stop_reason = None
        for chunk in response_stream:
            if chunk.candidates:
                for cand in chunk.candidates:
                    if cand.finish_reason:
                        stop_reason = getattr(cand.finish_reason, 'name', cand.finish_reason)
        
        if stop_reason:
            stop_reasons[stop_reason] += 1
            if "MALFORMED_FUNCTION_CALL" in str(stop_reason):
                mfc_count += 1
        else:
            stop_reasons["UNKNOWN"] += 1
            
        success_runs += 1
        print(f"Stop Reason: {stop_reason}")
        i += 1
        # Small delay between calls
        time.sleep(1)
        
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg or "Resource exhausted" in err_msg:
            print(f"\n[429 Resource Exhausted] Sleeping 15 seconds before retrying run {i}...")
            time.sleep(15)
        else:
            print(f"\nError during run {i}: {e}")
            i += 1
            time.sleep(2)

print("\n" + "=" * 50)
print(f"【Evaluation finished】 Total runs: {NUM_RUNS}")
print(f"Success runs: {success_runs}")
print(f"MALFORMED_FUNCTION_CALL count: {mfc_count}")
print(f"MALFORMED_FUNCTION_CALL rate: {(mfc_count / success_runs) * 100:.2f}%")
print("All Stop Reasons:")
for reason, count in stop_reasons.items():
    print(f"  - {reason}: {count}")
print("=" * 50)
