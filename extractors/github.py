"""GitHub repository extraction via web scraping."""

import requests
from bs4 import BeautifulSoup

import config
from extractors.base import BaseExtractor, ExtractionResult
from extractors.detector import extract_github_parts


class GitHubExtractor(BaseExtractor):
    """Extract GitHub repository content via API and scraping."""

    def extract(self, url: str) -> ExtractionResult:
        parts = extract_github_parts(url)
        if not parts:
            return self._scrape_page(url)

        owner, repo = parts["owner"], parts["repo"]
        return self._extract_repo(owner, repo, url)

    def _extract_repo(self, owner: str, repo: str, url: str) -> ExtractionResult:
        """Extract repo info via GitHub API (no auth needed for public repos)."""
        headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": config.USER_AGENT}
        sections = []

        # Repo metadata
        resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            sections.append(f"Repository: {data.get('full_name', f'{owner}/{repo}')}")
            sections.append(f"Description: {data.get('description', 'N/A')}")
            sections.append(f"Stars: {data.get('stargazers_count', 0)}")
            sections.append(f"Language: {data.get('language', 'N/A')}")
            sections.append(f"Topics: {', '.join(data.get('topics', []))}")
            sections.append(f"License: {data.get('license', {}).get('name', 'N/A') if data.get('license') else 'N/A'}")
            sections.append(f"Last updated: {data.get('updated_at', 'N/A')}")
            title = data.get("full_name", f"{owner}/{repo}")
        else:
            title = f"{owner}/{repo}"
            sections.append(f"Repository: {owner}/{repo}")
            sections.append("(Could not fetch metadata via API)")

        # README
        for readme_path in ["README.md", "readme.md", "README.rst", "README"]:
            resp = requests.get(
                f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{readme_path}",
                headers={"User-Agent": config.USER_AGENT},
                timeout=15,
            )
            if resp.status_code == 200:
                sections.append(f"\n--- README ---\n{resp.text[:8000]}")
                break

        # File tree (top-level)
        resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/",
            headers=headers,
            timeout=15,
        )
        if resp.status_code == 200:
            items = resp.json()
            tree = "\n".join(f"  {'[dir] ' if item['type'] == 'dir' else ''}{item['name']}" for item in items[:50])
            sections.append(f"\n--- File Structure ---\n{tree}")

        raw_content = "\n".join(sections)

        return ExtractionResult(
            title=title,
            url=url,
            source_type="GitHub",
            raw_content=raw_content,
            metadata={"owner": owner, "repo": repo},
        )

    def _scrape_page(self, url: str) -> ExtractionResult:
        """Fallback: scrape the GitHub page directly."""
        resp = requests.get(url, headers={"User-Agent": config.USER_AGENT}, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")

        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "GitHub Page"

        # Get the main article/readme content
        article = soup.find("article") or soup.find("div", {"role": "main"}) or soup.body
        text = article.get_text(separator="\n", strip=True) if article else soup.get_text(separator="\n", strip=True)

        return ExtractionResult(
            title=title.replace(" · GitHub", ""),
            url=url,
            source_type="GitHub",
            raw_content=text[:10000],
            metadata={},
        )
