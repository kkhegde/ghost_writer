import json
from googleapiclient.discovery import build
from docx import Document
import requests
from bs4 import BeautifulSoup
from typing import List
from io import BytesIO
from docx.shared import Inches
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from docx2pdf import convert
import os

CONFIG_FILE = ".\\config.json"
BLOG_POST_LIST = ".\\test_output\\blog_post_urls.txt"
PAGE_LOAD_WAIT = 20

def get_travel_blog_urls() -> List[str]:
    # Load the configuration file
    with open(CONFIG_FILE, "r") as config_file:
        config = json.load(config_file)

    # Fetch API Key and Blog ID from the configuration file
    BLOGGER_API_KEY = config['BLOGGER_API_KEY']
    TRAVEL_BLOG_ID = config['TRAVEL_BLOG_ID']

    # Create a service to interact with Blogger API
    service = build('blogger', 'v3', developerKey=BLOGGER_API_KEY)

    # Request to get all posts from the blog with pagination
    post_links = []
    request = service.posts().list(blogId=TRAVEL_BLOG_ID, maxResults=100)  # Request up to 100 posts per page
    while request is not None:
        response = request.execute()
        for post in response.get('items', []):
            post_url = post.get('url', '').lower()
            if 'second-post' not in post_url and 'first-post' not in post_url:  # Ignore posts with 'second-post' and 'first-post' in the URL
                post_links.append(post['url'])
        request = service.posts().list_next(request, response)  # Get the next page of posts

    return list(reversed(post_links))

def download_and_add_image(doc, img_src, element):
    try:
        img_response = requests.get(img_src)
        if img_response.status_code == 200:
            image_stream = BytesIO(img_response.content)
            doc.add_picture(image_stream, width=Inches(5.0))
            # Add the image title or alt text as caption
            caption = element.get('title') or element.get('alt', 'No description available')
            if caption != 'No description available':
                doc.add_paragraph(caption, style='Caption')

    except Exception as img_e:
        print(f"Failed to download image: {img_src}, error: {img_e}")

def download_and_add_map(doc, map_src, element):
    try:
        # Construct a Google Static Maps API URL
        base_url = "https://maps.googleapis.com/maps/api/staticmap"
        # Load the configuration file
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
        api_key = config['GMAPS_API_KEY']  # Replace with your actual API key

        # Get width and height from iframe tag
        width = element.get('width', '640')
        height = element.get('height', '480')
        size = f"{width}x{height}"

        # Parameters for the static map (you may need to adjust these)
        params = {
            "center": "0,0",  # Default center (can be adjusted based on iframe content if possible)
            "zoom": "14",
            "size": size,
            "key": api_key
        }
        map_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        print(f"map url = {map_url}")

        # Request the static map image
        map_response = requests.get(map_url)
        if map_response.status_code == 200:
            map_stream = BytesIO(map_response.content)
            doc.add_picture(map_stream, width=Inches(4.0))

            # Add the map alt and title text if available
            alt_text = element.get('alt', 'Map description not available')
            title_text = element.get('title', 'Map title not available')
            doc.add_paragraph(f'Map description: {alt_text}')
            doc.add_paragraph(f'Map title: {title_text}')
    except Exception as map_e:
        print(f"Failed to download map: {map_src}, error: {map_e}")

def download_and_add_map_sshot(doc, title, map_src, element):
    try:
        # Set up Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        print(f"loading map at {map_src} in page {title}")
        # Load the map page
        driver.get(map_src)

        # Wait for the page to load completely
        time.sleep(PAGE_LOAD_WAIT)

        # Wait until the map iframe is loaded
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))

        # Take a screenshot of the map
        screenshot = driver.get_screenshot_as_png()
        map_stream = BytesIO(screenshot)

        # Add the screenshot to the document
        doc.add_picture(map_stream, width=Inches(6.0))

        # Close the driver
        driver.quit()

    except Exception as map_e:
        print(f"Failed to download map: {map_src}, error: {map_e}")

def set_font_to_aptos(doc):
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.name = 'Aptos'
            r = run._element
            rPr = r.get_or_add_rPr()
            rFonts = OxmlElement('w:rFonts')
            rFonts.set(qn('w:ascii'), 'Aptos')
            rFonts.set(qn('w:hAnsi'), 'Aptos')
            rFonts.set(qn('w:eastAsia'), 'Aptos')
            rFonts.set(qn('w:cs'), 'Aptos')
            rPr.append(rFonts)

def create_travel_blog_docx(output_docx_path):
    # Load URLs from the text file
    with open(BLOG_POST_LIST, "r", encoding="utf-8") as file:
        post_links = [line.strip() for line in file.readlines()]

    # Create a new Word document
    doc = Document()
    doc.add_heading("Travel Blog Posts", level=1)

    # Iterate through each post URL and get the content
    first_time = True

    for link in post_links:
        if first_time:
            first_time = False
        else:
            doc.add_page_break()

        try:
            # Request the blog post page
            response = requests.get(link)
            if response.status_code == 200:
                # Parse the post HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find("title").get_text().replace("Travel diaries: ", "") if soup.find("title") else "No Title"
                doc.add_heading(title, level=2)
                
                # Find and add all headings, paragraphs, and images from the post body
                post_body = soup.find("div", class_="post-body")
                if post_body:
                    for element in post_body.descendants:
                        if element.name == 'h1':
                            doc.add_heading(element.get_text(), level=1)
                        elif element.name == 'h2':
                            doc.add_heading(element.get_text(), level=2)
                        elif element.name == 'h3':
                            doc.add_heading(element.get_text(), level=3)
                        elif element.name == 'p':
                            if element.get_text(strip=True):  # Add paragraph text if not empty
                                doc.add_paragraph(element.get_text())
                        elif element.name == 'img':
                            img_src = element.get('src')
                            if img_src:
                                if img_src.startswith("https://blogger.googleusercontent.com/"):
                                    download_and_add_image(doc, img_src, element)
                        elif element.name == 'iframe':
                            map_src = element.get('src')
                            if map_src and map_src.startswith("https://www.google.com/maps"):
                                # download_and_add_map(doc, map_src, element)
                                download_and_add_map_sshot(doc, title, map_src, element)
            else:
                print(f"Failed to load post: {link} - Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error processing {link}: {e}")

    # Set the font to Aptos for all paragraphs and headings
    set_font_to_aptos(doc)

    # Save the Word document
    doc.save(output_docx_path)

def create_travel_blog_docx_split(output_docx_path):
    # Load URLs from the text file
    with open(BLOG_POST_LIST, "r", encoding="utf-8") as file:
        post_links = [line.strip() for line in file.readlines()]

    chunk_size = 1
    chunks = [post_links[i:i + chunk_size] for i in range(0, len(post_links), chunk_size)]

    for idx, chunk in enumerate(chunks):
        doc = Document()
        first_time = True

        for link in chunk:
            if first_time:
                first_time = False
            else:
                doc.add_page_break()

            try:
                # Request the blog post page
                response = requests.get(link)
                if response.status_code == 200:
                    # Parse the post HTML
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.find("title").get_text().replace("Travel diaries: ", "") if soup.find("title") else "No Title"
                    doc.add_heading(title, level=2)

                    # Find and add all headings, paragraphs, and images from the post body
                    post_body = soup.find("div", class_="post-body")
                    if post_body:
                        for element in post_body.descendants:
                            if element.name == 'h1':
                                doc.add_heading(element.get_text(), level=1)
                            elif element.name == 'h2':
                                doc.add_heading(element.get_text(), level=2)
                            elif element.name == 'h3':
                                doc.add_heading(element.get_text(), level=3)
                            elif element.name == 'p':
                                if element.get_text(strip=True):  # Add paragraph text if not empty
                                    doc.add_paragraph(element.get_text())
                            elif element.name == 'img':
                                img_src = element.get('src')
                                if img_src:
                                    if img_src.startswith("https://blogger.googleusercontent.com/"):
                                        download_and_add_image(doc, img_src, element)
                            elif element.name == 'iframe':
                                map_src = element.get('src')
                                if map_src and map_src.startswith("https://www.google.com/maps"):
                                    download_and_add_map_sshot(doc, title, map_src, element)
                else:
                    print(f"Failed to load post: {link} - Status Code: {response.status_code}")
            except Exception as e:
                print(f"Error processing {link}: {e}")

        # Set the font to Aptos for all paragraphs and headings
        set_font_to_aptos(doc)

        # Save the Word document
        doc_name = os.path.join(output_docx_path, f'travel_blog_posts_{idx + 1:02}.docx')
        doc.save(doc_name)

def convert_docx_to_pdf(docx_file_path, pdf_file_path) -> str:
    try:
        convert(docx_file_path, pdf_file_path)
        return f"Successfully converted {docx_file_path} to {pdf_file_path}"
    except Exception as e:
        return f"Failed to convert {docx_file_path} to PDF: {e}"

def convert_docx_to_pdf_multi(docx_path, pdf_path, docx_file_name_starts_with) -> None:
    try:
        for file_name in os.listdir(docx_path):
            if file_name.startswith(docx_file_name_starts_with) and file_name.endswith('.docx'):
                docx_file = os.path.join(docx_path, file_name)
                pdf_file = os.path.join(pdf_path, f"{os.path.splitext(file_name)[0]}.pdf")
                convert(docx_file, pdf_file)
                print(f"Successfully converted {docx_file} to {pdf_file}")
    except Exception as e:
        print(f"Failed to convert documents starting with {docx_file_name_starts_with} to PDFs: {e}")

if __name__ == "__main__":
    # Define the output file path
    output_file_path = ".\\test_output\\blog_post_urls.txt"

    # Write all blog post URLs to the file in reverse order (oldest first)
    post_links = get_travel_blog_urls()
    with open(output_file_path, "w", encoding="utf-8") as file:
        for link in post_links:
            file.write(link + "\n")
        print(f"All blog post URLs have been saved to {output_file_path}")

    # Create a Word document with the blog posts
    # output_docx_file = ".\\test_output\\travel_blog_posts.docx"
    # create_travel_blog_docx(output_docx_file)
    # print(f"All blog post contents have been saved to {output_docx_file}")

    # output_pdf_file = ".\\test_output\\travel_blog_posts.pdf"
    # docx2pdf_convert_result = convert_docx_to_pdf(output_docx_file, output_pdf_file)
    # print(docx2pdf_convert_result)

    print("creating one docx per blog post")
    output_docx_path = ".\\test_output"
    create_travel_blog_docx_split(output_docx_path)

    # file_name_starts_with = "travel_blog_posts_"
    # convert_docx_to_pdf_multi(output_docx_path, output_docx_path, file_name_starts_with)
