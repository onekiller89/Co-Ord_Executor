"""General article/document extraction via web scraping."""

import requests
from bs4 import BeautifulSoup

try:
    from readability import Document as ReadabilityDocument
    HAS_READABILITY = True
except ImportError:
    HAS_READABILITY = False

import config
from extractors.base import BaseExtractor, ExtractionResult


class ArticleExtractor(BaseExtractor):
    """Extract article/document content via scraping with readability."""

    def extract(self, url: str) -> ExtractionResult:
        resp = requests.get(
            url,
            headers={"User-Agent": config.USER_AGENT},
            timeout=20,
            allow_redirects=True,
        )
        resp.raise_for_status()

        # Use readability-lxml for clean extraction if available
        if HAS_READABILITY:
            doc = ReadabilityDocument(resp.text)
            title = doc.title()
            html_content = doc.summary()
            soup = BeautifulSoup(html_content, "lxml")
            text = soup.get_text(separator="\n", strip=True)
        else:
            soup = BeautifulSoup(resp.text, "lxml")

            # Remove script/style noise
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else "Untitled Article"

            # Try to find the main article content
            article = (
                soup.find("article")
                or soup.find("main")
                or soup.find("div", {"role": "main"})
                or soup.find("div", class_=lambda c: c and "content" in c.lower() if c else False)
            )
            container = article or soup.body or soup
            text = container.get_text(separator="\n", strip=True)

        # Extract all links from the page
        links = []
        full_soup = BeautifulSoup(resp.text, "lxml")
        for a_tag in full_soup.find_all("a", href=True):
            href = a_tag["href"]
            link_text = a_tag.get_text(strip=True)
            if href.startswith("http") and link_text:
                links.append(f"{link_text}: {href}")

        raw_content = text[:12000]
        if links:
            raw_content += "\n\n--- Links found on page ---\n" + "\n".join(links[:30])

        return ExtractionResult(
            title=title,
            url=url,
            source_type="Article",
            raw_content=raw_content,
            metadata={},
        )
