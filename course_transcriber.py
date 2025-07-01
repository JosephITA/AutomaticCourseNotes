import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import whisper


def setup_driver(headless: bool = False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


def login(driver, url, username, password):
    driver.get(url)
    # Example selectors - these may need to be customized per site
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "form button[type=submit]").click()
    # Wait for login to complete
    time.sleep(5)


def download_video(video_element, download_dir):
    src = video_element.get_attribute("src")
    if not src:
        return None
    response = requests.get(src, stream=True)
    filename = os.path.join(download_dir, os.path.basename(src))
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return filename


def transcribe_video(video_path, transcript_dir, model):
    basename = os.path.splitext(os.path.basename(video_path))[0]
    result = model.transcribe(video_path)
    txt_path = os.path.join(transcript_dir, f"{basename}.txt")
    with open(txt_path, "w") as f:
        f.write(result.get("text", ""))
    return txt_path


def main():
    url = input("Course login URL: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    download_dir = os.path.join(os.getcwd(), "downloads")
    transcript_dir = os.path.join(os.getcwd(), "transcripts")
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(transcript_dir, exist_ok=True)

    driver = setup_driver()
    try:
        login(driver, url, username, password)

        # Replace this selector with one that matches your course's video elements
        video_elements = driver.find_elements(By.TAG_NAME, "video")
        if not video_elements:
            print("No videos found on the page.")
            return

        model = whisper.load_model("base")
        for idx, video in enumerate(video_elements, start=1):
            print(f"Processing video {idx}...")
            video_path = download_video(video, download_dir)
            if video_path is None:
                print("Could not download video.")
                continue
            txt = transcribe_video(video_path, transcript_dir, model)
            print(f"Transcript saved to {txt}")
            proceed = input("Proceed to next video? (y/n): ").strip().lower()
            if proceed != 'y':
                break
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
