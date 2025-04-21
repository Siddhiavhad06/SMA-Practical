import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import openpyxl

# Function to sanitize the filename (remove or replace invalid characters)
def sanitize_filename(filename):
    # Remove characters that are not allowed in filenames
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Function to download media (images or videos)
def download_media(url, media_folder, media_type="image"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Sanitize the filename to remove invalid characters
            media_name = os.path.join(media_folder, sanitize_filename(os.path.basename(url)))
            with open(media_name, 'wb') as file:
                file.write(response.content)
            print(f"{media_type.capitalize()} downloaded: {media_name}")
            return media_name  # Return the saved file path for logging
        else:
            print(f"Failed to download {media_type} from {url}")
            return None
    except Exception as e:
        print(f"Error downloading {media_type} from {url}: {e}")
        return None

# Function to scrape media (images and videos) from a webpage
def scrape_media(url, media_folder="internship"):  # Folder changed to "internship"
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Path to Desktop
    media_folder_path = os.path.join(desktop_path, media_folder)  # Internship folder on Desktop

    if not os.path.exists(media_folder_path):
        os.makedirs(media_folder_path)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }



    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code != 200:
        print(f"Failed to retrieve webpage: {url}")
        return

    

soup = BeautifulSoup(response.text, "html.parser")

    # Prepare Excel sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Media Data"
    ws.append(["Media Type", "URL", "File Path"])

    # Scrape images
    images = soup.find_all("img")
    for img in images:
        img_url = img.get("src")
        if img_url:
            img_url = urljoin(url, img_url)
            img_file_path = download_media(img_url, media_folder_path, media_type="image")
            if img_file_path:
                ws.append(["Image", img_url, img_file_path])

    # Scrape videos
    videos = soup.find_all("video")
    for video in videos:
        video_sources = video.find_all("source")
        for source in video_sources:
            video_url = source.get("src")
            if video_url:
                video_url = urljoin(url, video_url)
                # Handle different video formats if needed
                if video_url.endswith(('.mp4', '.webm', '.ogg')):
                    video_file_path = download_media(video_url, media_folder_path, media_type="video")
                    if video_file_path:
                        ws.append(["Video", video_url, video_file_path])

    # Save Excel sheet
    excel_file = os.path.join(media_folder_path, "media_info.xlsx")
    wb.save(excel_file)
    print(f"Media information saved to {excel_file}")

if __name__ == "__main__":
    website_url = "https://www.videvo.net/stock-video-footage"  # Example URL
    scrape_media(website_url)

