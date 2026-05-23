"""Pytest collection guard for `scratch/`.

Files in this directory are experimental snapshots (test_temp*, taewon_human,
yugin_chatgpt) that were written against earlier op schemas and now fail at
module-load time (Pydantic validation errors on outdated literal/enum types,
or extra-forbidden fields like `sentenceId`).

We keep them on disk for historical reference / future migration, but tell
pytest to skip collection so the regular suite stays green.

To run one of them deliberately: `python -m pytest --override-ini='collect_ignore_glob=' nlp_server/opsspec/tests/scratch/<file>.py`.
"""

collect_ignore_glob = ["*.py"]
