# Reddit-to-NotebookLM Automated Insight Extractor

This repository contains a simple Python utility for exporting Reddit threads so they can be ingested into [NotebookLM](https://notebooklm.google.com/) or any other LLM-based analysis tool.

## Features

- Fetches posts from one or more subreddits using the Reddit API (via [PRAW](https://praw.readthedocs.io/)).
- Filters posts by score and optional keywords.
- Collects top-level comments for additional context.
- Saves results as JSON files in a local `data/` directory.

> **Note**: NotebookLM does not currently provide a public API for direct uploads. The exported JSON files can be manually imported into NotebookLM for summarization and insight extraction.

## Setup

1. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a Reddit application to obtain `client_id` and `client_secret`. Set the following environment variables (e.g. in your shell or with a `.env` file):

   ```bash
   export REDDIT_CLIENT_ID="your_client_id"
   export REDDIT_CLIENT_SECRET="your_client_secret"
   export REDDIT_USER_AGENT="reddit-to-notebooklm"
   export SUBREDDITS="python,technology"  # comma separated list
   export OUTPUT_DIR="data"  # optional, defaults to ./data
   ```

3. Run the exporter:

   ```bash
   python -m reddit_to_notebooklm.reddit_export
   ```

Exported JSON files will be written to the `data/` directory with a timestamped filename for each subreddit.

## Roadmap

This is an early prototype. Future improvements might include:

- Enhanced scoring using NLP techniques.
- Automated upload or integration with NotebookLM when an API becomes available.
- Additional export formats (Markdown, CSV, etc.).

