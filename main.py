import argparse
from scraper.scrape_airbnb import scrape_airbnb

def parse_args():
    parser = argparse.ArgumentParser(description='Write messages to a file in the specified format.')
    parser.add_argument('-f', '--format', type=str, choices=['csv', 'openai-json'], default='openai-json', help='Output format: csv or openai-json (default: openai-json)')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    output_format = args.format

    scrape_airbnb(output_format)
