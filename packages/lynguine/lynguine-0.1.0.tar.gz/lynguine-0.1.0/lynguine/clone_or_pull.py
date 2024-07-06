#!/usr/bin/env python

import argparse
import sys
from linguine.access.download import GitDownloader 
from linguine.config.settings import Settings

def main():
    parser = argparse.ArgumentParser(description="Git Repository Downloader")
    parser.add_argument('git_url', help="URL of the git repository to clone or pull")
    parser.add_argument('--cache_path', default="./repo_cache", help="Path to cache the repository")
    
    args = parser.parse_args()

    # Dummy settings and data_resources for GitDownloader
    settings = Settings()
    settings["default_cache_path"] =  args.cache_path
    data_resources = {"example_data": {}}
    data_name = "example_data"  # Replace with actual data name if applicable

    # Initialize and use GitDownloader
    try:
        downloader = GitDownloader(settings, data_resources, data_name, args.git_url)
        downloader._process_data()
        print(f"Repository processed successfully at {args.cache_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
