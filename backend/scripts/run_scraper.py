from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.scraping.scrape_jobs import scrape_jobs


if __name__ == "__main__":
    output = scrape_jobs()
    print(f"Raw file generated at: {output}")
