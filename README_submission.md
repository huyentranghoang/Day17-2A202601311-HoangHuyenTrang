# Lab 17 Submission Notes

Practice benchmark: **11/11 PASS** (hit rate 100%). Memory vs no-memory: 100% vs 18.2%.

## 3 required questions

1. **Most important layer in this test set:** `long_term` — it unlocks E02 preference, E03 open loop, E08 recency (BLUEBIRD-42 → TypeScript/NestJS), and E09 isolation (Lan/LOTUS-88 must not leak ORCHID-27). Without it, cross-session cases collapse.

2. **Context Block / Zep vs Redis+Qdrant:** Zep Context Block + graph search gives relevance-ranked facts, validity ranges, and managed ingestion/polling. Redis+Qdrant is transparent and local, but you own windowing, conflict/recency, and indexing — more control, more ops. Lab uses Zep as primary durable memory; Redis/Qdrant as the “build your own” baseline.

3. **Guardrail against memory poisoning:** require consent (`memory_opt_in`) before durable write; redact PII on ingest; scope every long-term/episodic call by `user_id`; prefer recency with provenance over blind overwrite; heartbeat/maintenance must not invent new high-impact preferences without review; right-to-be-forgotten deletes user-scoped stores only.

## Benchmark analysis (4 questions)

1. **Lowest layer hit rate (student):** all layers 100% on practice. No-memory baseline fails every durable layer; only short_term (E01, E10) passes — so cross-session/episodic/semantic are the weak layers without memory.
2. **Most retrieved tokens:** E02 long_term (~1362 tokens), then E03 (~1347) and E08 (~1304).
3. **E07 mixed** needs **long_term + semantic**: personal `Python` preference plus shared `Idempotency-Key` payment rule.
4. **Token reduction:** student avg ~14.2%; no-memory ~81.8% but hit rate only 18.2%. High reduction without evidence is empty context, not efficiency.

## E08 recency & E10 compaction

- **E08:** after stage-3 update, BLUEBIRD-42 backend is TypeScript/NestJS; older Python preference stays for ORCHID-27 — recency wins per project scope.
- **E10:** sliding window + durable notes keep `REVIEW-DEADLINE-1600` / Friday 16:00 after filler turns evict raw messages; buffer alone would drop the constraint.

## Privacy

Ran `python -m src.forget --user-id minh-lab17` then `--verify-only`: `Zep user absent: True`, `Redis user keys remaining: 0`. Benchmark reports were saved before delete.
