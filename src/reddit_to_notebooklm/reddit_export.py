"""Reddit thread retrieval and export to NotebookLM-compatible format."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, List, Optional

import praw


def _env(var: str, default: Optional[str] = None) -> str:
    value = os.getenv(var)
    if value is None:
        if default is not None:
            return default
        raise EnvironmentError(f"Missing environment variable: {var}")
    return value


@dataclass
class SubredditConfig:
    name: str
    limit: int = 10
    score_threshold: int = 0
    keywords: List[str] = field(default_factory=list)


@dataclass
class Config:
    client_id: str
    client_secret: str
    user_agent: str
    subreddits: List[SubredditConfig]
    output_dir: str = "data"

    @staticmethod
    def from_env() -> "Config":
        subreddits = os.getenv("SUBREDDITS", "").split(",")
        sub_configs = [SubredditConfig(name=s.strip()) for s in subreddits if s.strip()]
        return Config(
            client_id=_env("REDDIT_CLIENT_ID"),
            client_secret=_env("REDDIT_CLIENT_SECRET"),
            user_agent=_env("REDDIT_USER_AGENT", "reddit-to-notebooklm"),
            subreddits=sub_configs,
            output_dir=os.getenv("OUTPUT_DIR", "data"),
        )


class RedditExporter:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.reddit = praw.Reddit(
            client_id=cfg.client_id,
            client_secret=cfg.client_secret,
            user_agent=cfg.user_agent,
        )
        os.makedirs(cfg.output_dir, exist_ok=True)

    def run(self) -> None:
        for sub_cfg in self.cfg.subreddits:
            self._export_subreddit(sub_cfg)

    def _export_subreddit(self, sub_cfg: SubredditConfig) -> None:
        subreddit = self.reddit.subreddit(sub_cfg.name)
        submissions = subreddit.hot(limit=sub_cfg.limit)
        posts = []
        for submission in submissions:
            if submission.score < sub_cfg.score_threshold:
                continue
            if sub_cfg.keywords and not any(k.lower() in submission.title.lower() for k in sub_cfg.keywords):
                continue
            post = {
                "id": submission.id,
                "title": submission.title,
                "score": submission.score,
                "url": submission.url,
                "created_utc": submission.created_utc,
                "selftext": submission.selftext,
                "comments": self._get_comments(submission, limit=20),
            }
            posts.append(post)
        if not posts:
            return
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(self.cfg.output_dir, f"{sub_cfg.name}_{ts}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"Exported {len(posts)} posts from r/{sub_cfg.name} -> {out_path}")

    def _get_comments(self, submission, limit: int = 20) -> List[dict]:
        submission.comments.replace_more(limit=0)
        comments = []
        for comment in submission.comments.list()[:limit]:
            comments.append(
                {
                    "id": comment.id,
                    "body": comment.body,
                    "score": comment.score,
                }
            )
        return comments


if __name__ == "__main__":
    cfg = Config.from_env()
    exporter = RedditExporter(cfg)
    exporter.run()
