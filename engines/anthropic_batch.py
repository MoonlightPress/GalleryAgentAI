"""anthropic_batch.py — shared Message Batches orchestration for the
translation engines (50% of standard pricing; latency-irrelevant at the end
of a monthly unattended pipeline).

The lifecycle every batched engine shares:
  1. If a pending file holds a batch id from a prior run, resume it —
     those results are already paid for; re-submitting would buy them twice.
  2. Otherwise submit the requests as one batch and persist its id BEFORE
     polling, so a killed process can't orphan a paid-for batch.
  3. Poll until the batch ends or max_wait passes. A timeout is reported,
     not raised: the pipeline's remaining steps must continue, and the
     pending file carries the batch into the next run.

What is NOT shared: building requests and applying results — each engine
owns its prompt shape and its apply-by-id/apply-by-string logic. The one
contract the caller must honor: results must be applicable independent of
chunk composition, because a resumed batch may be applied against data that
shifted since submission.
"""

import json
import time
from pathlib import Path


def read_pending(pending_path) -> str | None:
    p = Path(pending_path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("batch_id")
    except (json.JSONDecodeError, OSError):
        return None


def submit_or_resume(client, requests, pending_path) -> str:
    """Return the batch id to poll — the prior run's unfetched batch if one
    is pending, else a freshly submitted one (id persisted before return)."""
    pending_id = read_pending(pending_path)
    if pending_id:
        print(f"Resuming pending batch {pending_id} from a previous run.")
        return pending_id

    print(f"Submitting {len(requests)} request(s) as one Message Batch "
          f"(50% of standard pricing)...")
    batch = client.messages.batches.create(requests=requests)
    Path(pending_path).parent.mkdir(parents=True, exist_ok=True)
    Path(pending_path).write_text(
        json.dumps({"batch_id": batch.id}), encoding="utf-8")
    print(f"Batch {batch.id} submitted.")
    return batch.id


def wait_for_batch(client, batch_id, pending_path,
                   poll_interval=60, max_wait=75 * 60) -> bool:
    """Poll until the batch ends. False on timeout (pending file kept)."""
    waited = 0
    while True:
        status = client.messages.batches.retrieve(batch_id).processing_status
        if status == "ended":
            return True
        if waited >= max_wait:
            print(f"WARNING: batch {batch_id} still {status} after "
                  f"{waited // 60} min — giving up for this run. The batch id "
                  f"is saved in {pending_path}; the next run will fetch its "
                  f"results (no re-spend).")
            return False
        time.sleep(poll_interval)
        waited += max(poll_interval, 1)


def iter_succeeded_texts(client, batch_id):
    """Yield (custom_id, response_text) for succeeded results; print failures."""
    for result in client.messages.batches.results(batch_id):
        if result.result.type != "succeeded":
            print(f"  {result.custom_id}: {result.result.type}")
            continue
        text = next((b.text for b in result.result.message.content
                     if getattr(b, "type", "") == "text"), "")
        yield result.custom_id, text


def clear_pending(pending_path):
    Path(pending_path).unlink(missing_ok=True)
