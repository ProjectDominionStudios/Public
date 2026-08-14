# The Pascal Frontier — Whitepaper #1

## Modern AI Inference on Hardware That Apparently Didn't Get the Retirement Memo

This Founder-approved publication investigates vLLM and llama.cpp on an NVIDIA
Tesla V100 32 GB (Volta / SM70) system named Lurch. It documents successful
paths, failures, compatibility work, thermal and power observations, and the
evidence boundaries behind every material claim.

Mostly for engineers. Translated throughout for family, friends, leaders, and
curious humans who did not voluntarily memorize CUDA compatibility tables.

## Read the whitepaper

- [PDF](publication/The-Pascal-Frontier-WP1.pdf)
- [Editable DOCX](publication/The-Pascal-Frontier-WP1.docx)
- [Publication metadata](publication/The-Pascal-Frontier-WP1.machine.yaml)
- [Evidence and reference manifest](publication/evidence-reference-manifest.yaml)

## Evidence

The [`evidence/`](evidence/) directory is the privacy-sanitized, deduplicated
public projection of the WP1 handoff package. It includes:

- observed run logs, summaries, metrics, and thermal data;
- reproducibility scripts preserved with the runs;
- [`source-manifest.csv`](evidence/source-manifest.csv), mapping private archive
  entries to their public derivatives and hashes;
- [`claim-ledger.csv`](evidence/claim-ledger.csv), linking publication claims to
  supporting records; and
- [`redaction-ledger.md`](evidence/redaction-ledger.md), documenting privacy
  transformations, deduplication, and exclusions.

SGLang evidence is excluded because it belongs to Whitepaper #2. The private
Founder handoff remains the archival authority for original containers.

## Physical reference images

The [`images/`](images/) directory contains the approved Lurch physical
references copied from the canonical private ANTON.AOS evidence record:

- assembled dual-GPU interior; and
- cleaned front-airflow view with the `23.8` controller display preserved.

The photographs establish visible physical details only. They do not prove
unreadable labels, hidden devices, filesystem state, or operating behavior.

## Human and AI authority

J. Scott Henderson selected the scope, supplied the evidence, analyzed and
approved or rejected changes, and gave final publication approval. AI systems
assisted with exploration, drafting, visual production, evidence collation,
render QA, and packaging. AI did not autonomously approve claims or publication.

See the machine-readable metadata for the model and role ledger.
