import re
import sys
import os
import asyncio
import aiohttp
from urllib.parse import urljoin
from aiofiles import open as aioopen

IMG_HTML_PATTERN = re.compile(r'<img [^>]*src=["\']([^"\']+)["\']', re.IGNORECASE)
CSS_URL_PATTERN = re.compile(r'url\(["\']?([^"\')]+?\.(?:jpg|jpeg|png|gif|bmp|webp))["\']?\)', re.IGNORECASE)

async def fetch_content(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def fetch_binary_content(session, url):
    try:
        async with session.get(url) as response:
            return await response.read()
    except Exception as e:
        print(f"Error fetching binary content from {url}: {e}")
        return None

def extract_images_from_html(content, base_url):
    return [urljoin(base_url, img_url) for img_url in IMG_HTML_PATTERN.findall(content)]

def extract_images_from_css(content, base_url):
    return [urljoin(base_url, css_url) for css_url in CSS_URL_PATTERN.findall(content)]

async def download_image(session, url, output_dir):
    img_data = await fetch_binary_content(session, url)
    if img_data:
        img_name = os.path.basename(url.split('?')[0])
        img_path = os.path.join(output_dir, img_name)
        try:
            async with aioopen(img_path, 'wb') as f:
                await f.write(img_data)
            print(f"Downloaded: {url}")
        except Exception as e:
            print(f"Failed to save image {url}: {e}")
    else:
        raise Exception("Failed to download image")

async def fetch_images_from_url(url, output_dir):
    async with aiohttp.ClientSession() as session:
        html_content = await fetch_content(session, url)
        if not html_content:
            raise Exception("Failed to fetch main page")

        html_images = extract_images_from_html(html_content, url)

        css_links = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)["\']', html_content)
        css_images = []
        for css_url in css_links:
            css_url = urljoin(url, css_url)
            css_content = await fetch_content(session, css_url)
            if css_content:
                css_images += extract_images_from_css(css_content, url)
            else:
                raise Exception("Failed to fetch CSS file")

        all_images = set(html_images + css_images)
        print(f"Found {len(all_images)} images")

        os.makedirs(output_dir, exist_ok=True)

        tasks = [download_image(session, img_url, output_dir) for img_url in all_images]
        await asyncio.gather(*tasks)

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_images.py <url> [output_dir]")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'images'

    asyncio.run(fetch_images_from_url(url, output_dir))

if __name__ == '__main__':
    main()