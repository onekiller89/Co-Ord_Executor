"""Base extractor interface."""

from dataclasses import dataclass, field


@dataclass
class ExtractionResult:
    """Raw extraction result before AI processing."""
    title: str
    url: str
    source_type: str
    raw_content: str
    metadata: dict = field(default_factory=dict)


class BaseExtractor:
    """Base class for all content extractors."""

    def extract(self, url: str) -> ExtractionResult:
        raise NotImplementedError
