import pytest
import sys
import os
from unittest.mock import patch
from urllib.parse import urljoin
from aioresponses import aioresponses
from fetch_images import fetch_images_from_url, main


@pytest.mark.asyncio
async def test_fetch_images_from_url():
    with aioresponses() as m:
        main_url = "https://example.com"
        main_html_content = '''
        <html>
            <head>
                <link rel="stylesheet" href="styles.css">
            </head>
            <body>
                <img src="image1.jpg">
                <img src="https://example.com/image2.png">
            </body>
        </html>
        '''
        m.get(main_url, status=200, body=main_html_content)

        css_url = urljoin(main_url, "styles.css")
        css_content = '''
        body {
            background-image: url("background.jpg");
        }
        '''
        m.get(css_url, status=200, body=css_content)

        m.get(urljoin(main_url, "image1.jpg"), status=200, body=b'FakeImageData1')
        m.get("https://example.com/image2.png", status=200, body=b'FakeImageData2')
        m.get(urljoin(main_url, "background.jpg"), status=200, body=b'FakeImageData3')

        output_dir = "test_images"
        await fetch_images_from_url(main_url, output_dir)

        assert os.path.exists(os.path.join(output_dir, "image1.jpg"))
        assert os.path.exists(os.path.join(output_dir, "image2.png"))
        assert os.path.exists(os.path.join(output_dir, "background.jpg"))

        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))
        os.rmdir(output_dir)

@pytest.mark.asyncio
async def test_fetch_images_from_url_with_404_main_page():
    with aioresponses() as m:
        main_url = "https://example.com"
        m.get(main_url, status=404)

        output_dir = "test_images"
        with pytest.raises(Exception, match="Failed to fetch main page"):
            await fetch_images_from_url(main_url, output_dir)

@pytest.mark.asyncio
async def test_fetch_images_from_url_with_404_css_file():
    with aioresponses() as m:
        main_url = "https://example.com"
        main_html_content = '''
        <html>
            <head>
                <link rel="stylesheet" href="styles.css">
            </head>
            <body>
                <img src="image1.jpg">
            </body>
        </html>
        '''
        m.get(main_url, status=200, body=main_html_content)

        css_url = urljoin(main_url, "styles.css")
        m.get(css_url, status=404)

        output_dir = "test_images"

        with pytest.raises(Exception, match="Failed to fetch CSS file"):
            await fetch_images_from_url(main_url, output_dir)

@pytest.mark.asyncio
async def test_fetch_images_from_url_with_500_image_download():
    with aioresponses() as m:
        main_url = "https://example.com"
        main_html_content = '''
        <html>
            <body>
                <img src="image1.jpg">
            </body>
        </html>
        '''
        m.get(main_url, status=200, body=main_html_content)

        m.get(urljoin(main_url, "image1.jpg"), status=500)

        output_dir = "test_images"

        with pytest.raises(Exception, match="Failed to download image"):
            await fetch_images_from_url(main_url, output_dir)


@pytest.mark.asyncio
async def test_fetch_images_from_url_no_images_found():
    with aioresponses() as m:
        main_url = "https://example.com"
        main_html_content = '''
        <html>
            <body>
                <p>No images here!</p>
            </body>
        </html>
        '''
        m.get(main_url, status=200, body=main_html_content)

        output_dir = "test_images"

        await fetch_images_from_url(main_url, output_dir)

        assert not os.path.exists(os.path.join(output_dir, "image1.jpg"))
        assert not os.path.exists(os.path.join(output_dir, "image2.png"))
        assert not os.path.exists(os.path.join(output_dir, "background.jpg"))


def test_main_with_only_url():
    with patch('sys.exit') as mock_exit:
        sys.argv = ['fetch_images.py', 'https://example.com']
        main()

        mock_exit.assert_not_called()


def test_main_with_url_and_output_dir():
    with patch('sys.exit') as mock_exit:
        sys.argv = ['fetch_images.py', 'https://example.com', 'test_images']
        main()
        mock_exit.assert_not_called()
