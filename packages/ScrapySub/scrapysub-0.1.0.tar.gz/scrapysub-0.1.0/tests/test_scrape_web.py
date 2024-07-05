# tests/test_scrape_web.py
import unittest
from ScrapySub.scrape_web import ScrapeWeb

class TestScrapeWeb(unittest.TestCase):
    def test_scrape(self):
        scraper = ScrapeWeb()
        scraper.scrape("https://myportfolio-five-tau.vercel.app/")
        content = scraper.get_all_text_content()
        self.assertTrue("Example Domain" in content)

if __name__ == "__main__":
    unittest.main()
