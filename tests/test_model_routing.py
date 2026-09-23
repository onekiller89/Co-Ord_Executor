"""The selected subscription model must keep an explicit API fallback."""

import unittest
from unittest.mock import patch

import config
from extractors.base import ExtractionResult
from processors import ai_processor


VALID = """### Summary
Source summary.
### Key Insights
- One insight.
### Actions
- [ ] Do something.
### Implementation Prompts
None
### Links & Resources
- https://example.org
### Tags
`#source`
### Category
Research"""


def _result():
    return ExtractionResult(title="Source", url="https://example.org", source_type="YouTube",
                            raw_content="Source text", metadata={})


class ModelRoutingTests(unittest.TestCase):
    def test_codex_is_used_when_available(self):
        with (
            patch.object(config, "MODEL_PROVIDER", "codex"),
            patch.object(config, "CODEX_MODEL", "gpt-6-astra"),
            patch.object(ai_processor, "_process_codex", return_value=VALID),
            patch("budget.record_subscription_run"),
        ):
            result = _result()
            self.assertEqual(ai_processor.process_extraction(result), VALID)
            self.assertEqual(result.metadata["analysis_model"], "gpt-6-astra")

    def test_anthropic_fallback_is_recorded_when_codex_fails(self):
        with (
            patch.object(config, "MODEL_PROVIDER", "codex"),
            patch.object(config, "ANTHROPIC_API_KEY", "test-key"),
            patch.object(config, "CLAUDE_MODEL", "claude-opus-5-5"),
            patch.object(ai_processor, "_process_codex", side_effect=RuntimeError("offline")),
            patch.object(ai_processor, "_process_anthropic", return_value=VALID),
        ):
            result = _result()
            self.assertEqual(ai_processor.process_extraction(result), VALID)
            self.assertEqual(result.metadata["analysis_model"], "claude-opus-5-5")


if __name__ == "__main__":
    unittest.main()
