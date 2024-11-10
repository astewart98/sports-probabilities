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
    media_item = soup.find('div', class_='media-item multiple')

    if media_item:
        first_image = media_item.find('img')
        if first_image and 'src' in first_image.attrs:
            image_url = first_image['src']
            print(image_url)
        else:
            print("No image found in the specified div.")
    else:
        print("The specified div with class 'media-item multiple' was not found.")

if __name__ == '__main__':
    main()
