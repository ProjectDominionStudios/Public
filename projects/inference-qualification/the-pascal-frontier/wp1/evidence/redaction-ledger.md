# Redaction and Deduplication Ledger

## Scope

This is a public, privacy-sanitized projection of Founder-supplied WP1 evidence. It preserves observed versions, models, commands, timestamps, result statuses, metrics, errors, and failure records. The Studio's private canonical archives remain authoritative.

## Privacy transformations

- Replaced the original local Linux username path with `/home/<USER>`.
- Replaced the Founder Windows profile path with `C:\\Users\\<USER>`.
- Replaced RFC1918 addresses found in textual logs with `<PRIVATE_IP>`.
- No passwords, API keys, bearer tokens, or private-key material were intentionally retained.

## Deduplication

Files with identical privacy-sanitized SHA-256 values appear once under `evidence/runs/`. Every original archive path and hash remains listed in `source-manifest.csv`. The corrected handoff contains two byte-identical vLLM evidence ZIPs; one is treated as the canonical source and the duplicate is recorded, not re-published.

## Exclusions

- The SGLang archive is reserved for WP2 and is not part of this WP1 projection.
- Historical RAR containers are retained in the private handoff but not unpacked here; corrected ZIP replacements supply the accessible records.
- Unrelated draft reports, founder photos, and design assets are not technical run evidence.
