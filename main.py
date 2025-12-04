#!/usr/bin/env python3
"""
Price Monitoring Dashboard

Full-stack price tracking app. Scrapes product prices daily and visualizes trends.

Usage:
    python main.py --url <target_url>
    python main.py --url "https://books.toscrape.com/"
"""

import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import re
from datetime import datetime


def extract_price(price_text):
    """Extract numeric price from text like '£51.77' or '$19.99'"""
    # Remove currency symbols and extract numbers
    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
    if price_match:
        return float(price_match.group())
    return None


def scrape_data(url):
    """
    Main scraping logic - Scrapes product prices for monitoring

    Args:
        url: Target URL to scrape

    Returns:
        pandas.DataFrame: Scraped data with columns: name, price, currency, timestamp, url
    """
    # Set headers to avoid bot detection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # books.toscrape.com structure (default example site)
    products = soup.select('article.product_pod')

    if products:
        # books.toscrape.com format
        for product in products:
            try:
                name = product.select_one('h3 a')['title']
                price_text = product.select_one('p.price_color').text.strip()

                # Extract currency and numeric price
                currency = price_text[0] if price_text else '$'
                price = extract_price(price_text)

                product_url = product.select_one('h3 a')['href']

                if price is not None:
                    data.append({
                        'name': name,
                        'price': price,
                        'currency': currency,
                        'timestamp': timestamp,
                        'url': product_url
                    })
            except (AttributeError, KeyError, IndexError, ValueError):
                continue

    # If no data found with books.toscrape structure, try generic patterns
    if not data:
        # Try generic product/price patterns
        for item in soup.select('[class*="product"], [class*="item"]')[:20]:
            try:
                name_elem = item.select_one('[class*="name"], [class*="title"], h3, h4')
                price_elem = item.select_one('[class*="price"]')

                if name_elem and price_elem:
                    price_text = price_elem.text.strip()
                    price = extract_price(price_text)
                    currency = '$' if '$' in price_text else '£' if '£' in price_text else '$'

                    if price is not None:
                        data.append({
                            'name': name_elem.text.strip(),
                            'price': price,
                            'currency': currency,
                            'timestamp': timestamp,
                            'url': url
                        })
            except (AttributeError, KeyError, ValueError):
                continue

    return pd.DataFrame(data)


def analyze_prices(df):
    """Calculate basic price statistics"""
    if len(df) == 0 or 'price' not in df.columns:
        return None

    stats = {
        'count': len(df),
        'mean': df['price'].mean(),
        'median': df['price'].median(),
        'min': df['price'].min(),
        'max': df['price'].max(),
        'std': df['price'].std()
    }
    return stats


def main():
    parser = argparse.ArgumentParser(description='Price Monitoring Dashboard')
    parser.add_argument(
        '--url',
        default='https://books.toscrape.com/',
        help='Target URL to scrape (default: books.toscrape.com)'
    )
    parser.add_argument('--output', default='output/results.csv', help='Output file path')

    args = parser.parse_args()

    # Auto-add https:// if missing
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"Monitoring prices from {url}...")
    df = scrape_data(url)

    # Save to CSV
    output_path = Path(args.output)
    output_path.parent.mkdir(exist_ok=True)

    # Append mode if file exists (for tracking over time)
    if output_path.exists():
        existing_df = pd.read_csv(output_path)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_csv(output_path, index=False)

    print(f"[OK] Tracked {len(df)} product prices")
    print(f"[OK] Saved to {output_path}")

    # Display statistics
    stats = analyze_prices(df)
    if stats:
        print(f"\n[DATA] Price Statistics:")
        print(f"   Count: {stats['count']}")
        print(f"   Mean: ${stats['mean']:.2f}")
        print(f"   Median: ${stats['median']:.2f}")
        print(f"   Min: ${stats['min']:.2f}")
        print(f"   Max: ${stats['max']:.2f}")

    # Display sample
    if len(df) > 0:
        print(f"\n[DATA] Sample data:")
        print(df.head())


if __name__ == '__main__':
    main()
