import sys
from bs4 import BeautifulSoup
import requests

def main():
    if len(sys.argv) != 2:
        print("Usage: python scrapeImage.py <url>")
        return

    url = sys.argv[1]

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Fetch the HTML content from the website
    team_logo_img = soup.find('img', class_='teamlogo')

    if team_logo_img and 'src' in team_logo_img.attrs:
        image_url = team_logo_img['src']
        print(image_url)
    else:
        print("The img tag with class 'teamlogo' was not found or has no src attribute.")

if __name__ == '__main__':
    main()
