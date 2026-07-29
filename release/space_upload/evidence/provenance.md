# Reproduction provenance

- Paper: arXiv `2605.19392`, OpenReview `4MVVscCjYu`
- Paper HTML retrieval: 2026-07-29
- HTML SHA-256: `c7ebf813dc871eba1c0c93542fcf0a7d599c7c4d44a543a0000270ce48ae7998`
- Source tar SHA-256: `9922a66ab5708f357aa8be09f207565791a6488f48b0d8d2cf27011964521265`
- Fixed command: `uv run --locked python repro/src/verify.py`
- Evidence Git SHA: `43327acebf41a3f13e73f2a57337e383eb87376c`
- Evidence run: `5c77ca17-87eb-4c40-8555-6a5be544ccce`
- Environment: uv lock, Python 3.12.13, NumPy 2.5.1
- Compute estimate: 8 CPU cores
- Selected compute: Hugging Face `cpu-upgrade`
- Actual allocation: cgroup quota 8 vCPU
- Wall time: 1m30s; verifier time 26.288s
- Determinism: fixed initial states; Claim 4 bootstrap seed `20260729`;
  Claim 5 CPU timing is explicitly non-scientific; Claim 6 has no RNG.

The raw directory is a byte-for-byte extraction from the marked `orx logs`
evidence stream. Every entry matches `raw/output_manifest.json`.
