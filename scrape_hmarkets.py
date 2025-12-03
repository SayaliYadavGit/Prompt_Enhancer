"""
Hantec Markets Website Scraper
Scrapes entire hmarkets.com website and creates knowledge base documents
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os
from pathlib import Path

class HantecWebsiteScraper:
    """Scrape hmarkets.com and create knowledge base files"""
    
    def __init__(self, base_url="https://hmarkets.com", output_dir="data/knowledge_base/website"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls = set()
        self.scraped_content = {}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Pages to prioritize
        self.priority_pages = [
            # Products & Services
            "/products/",
            "/trading-products/",
            "/forex/",
            "/metals/",
            "/indices/",
            "/commodities/",
            "/stocks/",
            "/cryptocurrencies/",
            
            # Trading Platforms
            "/trading-platforms/",
            "/trading-platforms/mt4-trading-platform/",
            "/trading-platforms/metatrader-5/",
            "/trading-platforms/hantec-markets-mobile-app/",
            "/trading-platforms/hantec-markets-web-trader/",
            "/trading-platforms/client-portal/",
            "/trading-platforms/hantec-social/",
            
            # Tools & Analysis
            "/tools/",
            "/tools/market-analysis/",
            "/tools/economic-calendar/",
            "/tools/trading-calculator/",
            "/tools/charts/",
            
            # Account Types
            "/account-types/",
            "/account-types/standard-account/",
            "/account-types/pro-account/",
            "/account-types/islamic-account/",
            "/account-types/demo-account/",
            
            # Education
            "/education/",
            "/education/trading-basics/",
            "/education/forex-trading/",
            "/education/cfd-trading/",
            "/education/technical-analysis/",
            "/education/fundamental-analysis/",
            "/education/risk-management/",
            "/education/trading-strategies/",
            "/education/webinars/",
            "/education/ebooks/",
            "/education/videos/",
            
            # About & Company
            "/about/",
            "/about/about-us/",
            "/about/why-hantec/",
            "/about/regulation/",
            "/about/awards/",
            "/about/careers/",
            "/about/contact-us/",
            
            # Support
            "/support/",
            "/faq/",
            "/help-center/",
            "/deposits/",
            "/withdrawals/",
            "/verification/",
            
            # Legal
            "/legal/",
            "/terms-and-conditions/",
            "/privacy-policy/",
            "/risk-warning/",
            "/complaints-procedure/",
            
            # Promotions
            "/promotions/",
            "/bonuses/",
            "/competitions/",
            
            # Partners
            "/partners/",
            "/ib-program/",
            "/affiliate-program/",
            "/white-label/",
        ]
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def extract_page_content(self, url):
        """Extract content from a single page"""
        try:
            print(f"Scraping: {url}")
            
            response = requests.get(
                url,
                timeout=10,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code != 200:
                print(f"  ❌ Failed: Status {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'noscript']):
                element.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text() if title else "Untitled"
            
            # Extract main content
            # Try different content containers
            main_content = (
                soup.find('main') or 
                soup.find('article') or 
                soup.find('div', class_='content') or
                soup.find('div', id='content') or
                soup.body
            )
            
            if not main_content:
                print(f"  ⚠️ No main content found")
                return None
            
            # Extract text
            text = main_content.get_text(separator='\n', strip=True)
            text = self.clean_text(text)
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ''
            
            if len(text) < 100:
                print(f"  ⚠️ Too short: {len(text)} chars")
                return None
            
            print(f"  ✅ Success: {len(text)} chars")
            
            return {
                'url': url,
                'title': title_text,
                'description': description,
                'content': text,
                'length': len(text)
            }
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            return None
    
    def get_page_category(self, url):
        """Determine category from URL"""
        path = urlparse(url).path.lower()
        
        if '/trading-platforms/' in path or '/platforms/' in path:
            return 'platforms'
        elif '/products/' in path or '/forex/' in path or '/metals/' in path or '/indices/' in path:
            return 'products'
        elif '/education/' in path or '/learn/' in path:
            return 'education'
        elif '/account' in path:
            return 'accounts'
        elif '/tools/' in path or '/calculator' in path or '/analysis' in path:
            return 'tools'
        elif '/about/' in path or '/company/' in path:
            return 'about'
        elif '/support/' in path or '/faq' in path or '/help' in path:
            return 'support'
        elif '/legal/' in path or '/terms' in path or '/privacy' in path:
            return 'legal'
        elif '/deposit' in path or '/withdraw' in path or '/fund' in path:
            return 'funding'
        elif '/partner' in path or '/ib' in path or '/affiliate' in path:
            return 'partners'
        else:
            return 'general'
    
    def scrape_priority_pages(self):
        """Scrape all priority pages"""
        print(f"\n🚀 Scraping {len(self.priority_pages)} priority pages...\n")
        
        for page_path in self.priority_pages:
            url = urljoin(self.base_url, page_path)
            
            if url in self.visited_urls:
                continue
            
            content = self.extract_page_content(url)
            
            if content:
                self.scraped_content[url] = content
                self.visited_urls.add(url)
            
            # Be respectful - wait between requests
            time.sleep(1)
        
        print(f"\n✅ Scraped {len(self.scraped_content)} pages successfully")
    
    def save_to_files(self):
        """Save scraped content to organized files"""
        print(f"\n💾 Saving content to files...\n")
        
        # Group by category
        categories = {}
        for url, content in self.scraped_content.items():
            category = self.get_page_category(url)
            if category not in categories:
                categories[category] = []
            categories[category].append(content)
        
        # Save each category to a file
        for category, contents in categories.items():
            filename = f"{category}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Hantec Markets - {category.title()}\n")
                f.write(f"# Total Pages: {len(contents)}\n")
                f.write(f"# Source: hmarkets.com\n\n")
                f.write("=" * 80 + "\n\n")
                
                for idx, content in enumerate(contents, 1):
                    f.write(f"\n{'=' * 80}\n")
                    f.write(f"PAGE {idx}: {content['title']}\n")
                    f.write(f"URL: {content['url']}\n")
                    f.write(f"{'=' * 80}\n\n")
                    
                    if content['description']:
                        f.write(f"Description: {content['description']}\n\n")
                    
                    f.write(content['content'])
                    f.write("\n\n")
            
            print(f"  ✅ {filename}: {len(contents)} pages ({sum(c['length'] for c in contents):,} chars)")
        
        # Create master index file
        index_path = os.path.join(self.output_dir, "_index.txt")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# Hantec Markets Knowledge Base Index\n")
            f.write(f"# Total Pages Scraped: {len(self.scraped_content)}\n")
            f.write(f"# Total Categories: {len(categories)}\n")
            f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for category, contents in sorted(categories.items()):
                f.write(f"\n## {category.title()} ({len(contents)} pages)\n")
                for content in contents:
                    f.write(f"  - {content['title']}\n")
                    f.write(f"    URL: {content['url']}\n")
        
        print(f"\n  ✅ _index.txt: Master index created")
        print(f"\n✅ All files saved to: {self.output_dir}")
    
    def generate_summary(self):
        """Generate summary statistics"""
        print(f"\n📊 SCRAPING SUMMARY")
        print(f"=" * 80)
        print(f"Total URLs scraped: {len(self.scraped_content)}")
        print(f"Total content size: {sum(c['length'] for c in self.scraped_content.values()):,} characters")
        
        # Category breakdown
        categories = {}
        for url, content in self.scraped_content.items():
            category = self.get_page_category(url)
            categories[category] = categories.get(category, 0) + 1
        
        print(f"\nPages by category:")
        for category, count in sorted(categories.items()):
            print(f"  {category.title()}: {count} pages")
        
        print(f"\n✅ Knowledge base ready for RAG system!")
        print(f"=" * 80)

def main():
    """Main scraping function"""
    print("=" * 80)
    print("HANTEC MARKETS WEBSITE SCRAPER")
    print("=" * 80)
    
    scraper = HantecWebsiteScraper()
    
    # Step 1: Scrape priority pages
    scraper.scrape_priority_pages()
    
    # Step 2: Save to organized files
    scraper.save_to_files()
    
    # Step 3: Show summary
    scraper.generate_summary()
    
    print("\n🎉 Done! Your knowledge base is ready.")
    print(f"📂 Location: {scraper.output_dir}")
    print("\nNext steps:")
    print("1. Review the files in data/knowledge_base/website/")
    print("2. Upload to your project")
    print("3. ChromaDB will automatically index them")
    print("4. Test your AI mentor!")

if __name__ == "__main__":
    main()