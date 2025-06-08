from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
from random import choice
import re
import html

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36"
]

news_orgs = [
    "Alt News",
    "DD News",
    "Firstpost",
    "Hindustan Times",
    "India Today",
    "Jagran Josh",
    "LiveMint",
    "Moneycontrol",
    "NDTV",
    "News18",
    "OpIndia",
    "PIB",
    "Scroll.in",
    "Telegraph India",
    "The Economic Times",
    "The Hindu",
    "The Indian Express",
    "The New Indian Express",
    "The Wire India",
    "ThePrint",
    "Times Now",
    "Times of India",
    "Tribune India"
]


def process(title, content):
    def clean_text(text):
        if not (type(text) is str):
            return text

        # 1. Whitespace trimming
        text = text.strip()

        # 2. Converts HTML entities and special characters to plain text
        text = html.unescape(text)

        # 3. Removes <iframe>, <script>, <div>, <style> tags and their content
        text = re.sub(r'<(iframe|script|div|style)[^>]*>.*?</\1>', '', text, flags=re.DOTALL|re.IGNORECASE)

        # 4. Removes promotional/unwanted phrases
        promotions = [
            'click here', 'Click Here', 'advertisement', 'Ad', 'Subscribe', 
            'Read More', 'Learn More', 'Join Now', 'Get Started', 'Sign Up', 
            'Click to Learn More', 'Buy Now', 'Limited Time Offer', 'Act Now', 
            'Don’t Miss Out', 'Exclusive Deal', 'Shop Now', 'Download Now', 
            'Try for Free', 'Free Trial', 'Register Now', 'See More', 
            'Follow Us', 'Stay Updated', 'Get Updates', 'Explore More', 
            'More Info', 'This Just In', 'Breaking News', 'Today’s Deals',
            'YOU MAY LIKE', 'Post comment', 'You can now subscribe to our Economic Times WhatsApp channel',
            'like and share', 'subscribe to our', 'follow us on', 'for more updates',
            'copyright', 'publisher:', 'advertisements', 'SUBSCRIBE NOW!'
        ]
        for phrase in promotions :
            text = text.replace(phrase, '')

        # 5. Removes "views are personal"
        text = re.sub(r'views?\s+are\s+personal', '', text, flags=re.IGNORECASE)

        # 6. Removes JS (function(){...})(...); blocks
        text = re.sub(r'\(function\s*\([^\)]*\)\s*\{.*?\}\s*\)\s*\([^\)]*\)\s*;?', '', text, flags=re.DOTALL)

        # 7. Removes https and www. links
        text = re.sub(r'https?://\S+|www\.\S+', '', text)

        # 8. Removes twitter links (pic.twitter.com)
        text = re.sub(r'pic\.twitter\.com/\S+', '', text)

        # 9. Removes news organization names
        for org in news_orgs:
            text = re.sub(rf'\b{re.escape(org)}\b', '', text, flags=re.IGNORECASE)

        # 10. Remove any remaining HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # 11. Remove invalid characters (non-ASCII and words containing unusual symbols)
        text = re.sub(r'[^\x00-\x7F]+', '', text)

        # 12. Clean up formatting
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space
        text = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', text)  # Add space before digits

        return text

    return clean_text(title), clean_text(content)


def get_details(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    
    chrome_options.add_argument(f'user-agent={choice(USER_AGENTS)}')
    # chrome_options.add_argument(f'--proxy-server=http://{choice(PROXIES)}')

    session = webdriver.Chrome(options=chrome_options)
    try:
        session.get(url)
        time.sleep(3)  # Time for JS to load

        html = session.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extract title
        page_title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # Extract article body
        article_body = ""

        script_tags = soup.find_all("script", {"type": "application/ld+json"})
        for tag in script_tags:
            try:
                data = json.loads(tag.string)
                if isinstance(data, dict) and "articleBody" in data:
                    article_body = data["articleBody"]
                    break
            except Exception:
                continue    # Some script tags may not be JSON

        final_content = article_body if article_body.strip() else ""

        return process(page_title, final_content)
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return "", ""
    finally:
        session.quit()

