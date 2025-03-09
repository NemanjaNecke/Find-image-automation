
import os
import time
import random
import argparse
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

def extract_candidate_info_from_results(driver):
    """
    Scans the current page for all anchor tags with an href attribute,
    then attempts to extract candidate title text from each.
    Returns the most common title (by frequency within this page) and one associated link.
    """
    wait = WebDriverWait(driver, 20)
    anchors = driver.find_elements(By.XPATH, "//a[@href]")
    candidates = []
    info_list = []  # list of (title, link) tuples
    for anchor in anchors:
        candidate_title = anchor.text.strip()
        if candidate_title:
            candidates.append(candidate_title)
            link = anchor.get_attribute("href")
            info_list.append((candidate_title, link))
    if candidates:
        counter = Counter(candidates)
        most_common_title, _ = counter.most_common(1)[0]
        for title, link in info_list:
            if title == most_common_title:
                return most_common_title, link
    return None, None

def process_image(image_path, driver):
    """
    In the current Google Lens tab, clicks the upload button, uploads the image,
    waits for results to load, and then extracts candidate info from the page.
    Returns a tuple (most_common_title, candidate_link) for that image.
    """
    wait = WebDriverWait(driver, 20)
    try:
        # Click the upload button using its visible text ("otpremite fajl")
        upload_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@role='button' and contains(text(),'otpremite fajl')]")
        ))
        driver.execute_script("arguments[0].click();", upload_button)
    except Exception as e:
        print(f"Error clicking upload button for {os.path.basename(image_path)}: {e}")
        return None, None

    try:
        # Locate file input element and send the image path.
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(image_path)
    except Exception as e:
        print(f"Error uploading file for {os.path.basename(image_path)}: {e}")
        return None, None

    # Wait for results to load – use a random delay to mimic human behavior.
    time.sleep(random.uniform(8, 12))

    title, link = extract_candidate_info_from_results(driver)
    return title, link

def process_images(folder_path, driver):
    """
    For each image in folder_path:
      - Open Google Lens in the main tab.
      - Duplicate the tab to work with a fresh instance.
      - Upload the image and extract candidate info from that page.
      - Close the duplicate tab and switch back to the main tab.
    Returns a list of tuples: (filename, most_common_title, candidate_link).
    """
    results = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")

            # Open Google Lens in the main tab.
            driver.get("https://lens.google.com")
            time.sleep(random.uniform(4, 6))

            # Duplicate the current tab.
            driver.execute_script("window.open('https://lens.google.com', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(random.uniform(4, 6))

            title, link = process_image(image_path, driver)
            results.append((filename, title, link))

            # Close duplicate tab and switch back to main.
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.uniform(5, 10))
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Extract book name from Google Lens search results for images in a folder."
    )
    parser.add_argument("folder", help="Path to the folder containing images.")
    parser.add_argument("output", help="Output file to save results.")
    args = parser.parse_args()

    folder_path = args.folder
    output_file = args.output

    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        exit(1)

    # Set up ChromeDriver with stealth options.
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    # Apply selenium-stealth to help mask automation.
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    try:
        results = process_images(folder_path, driver)
        # Write results per image to output file.
        with open(output_file, "w", encoding="utf-8") as f_out:
            for fname, title, link in results:
                f_out.write(f"{fname}: {title} | {link}\n")
    finally:
        driver.quit()

    print(f"\nDone! Results saved to '{output_file}'")

if __name__ == "__main__":
    main()
