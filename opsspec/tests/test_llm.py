from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from opsspec.core.llm import _openai_api_key


class LLMSecretTest(unittest.TestCase):
    def test_openai_api_key_prefers_secret_json_over_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            secret_path = Path(tmp) / "secret.json"
            secret_path.write_text('{"OPENAI_API_KEY": "from-secret"}', encoding="utf-8")

            with (
                patch("opsspec.core.llm._project_secret_path", return_value=secret_path),
                patch.dict(os.environ, {"OPENAI_API_KEY": "from-env"}, clear=False),
            ):
                self.assertEqual(_openai_api_key(), "from-secret")

    def test_openai_api_key_falls_back_to_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing_secret_path = Path(tmp) / "secret.json"

            with (
                patch("opsspec.core.llm._project_secret_path", return_value=missing_secret_path),
                patch.dict(os.environ, {"OPENAI_API_KEY": "from-env"}, clear=False),
            ):
                self.assertEqual(_openai_api_key(), "from-env")


if __name__ == "__main__":
    unittest.main()
