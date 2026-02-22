"""Content extractors for various source types."""

from extractors.detector import detect_source, SourceType
from extractors.youtube import YouTubeExtractor
from extractors.twitter import TwitterExtractor
from extractors.github import GitHubExtractor
from extractors.article import ArticleExtractor

EXTRACTORS = {
    SourceType.YOUTUBE: YouTubeExtractor,
    SourceType.TWITTER: TwitterExtractor,
    SourceType.GITHUB: GitHubExtractor,
    SourceType.ARTICLE: ArticleExtractor,
}


def get_extractor(url: str):
    """Return the appropriate extractor instance for a given URL."""
    source_type = detect_source(url)
    extractor_cls = EXTRACTORS[source_type]
    return extractor_cls(), source_type
