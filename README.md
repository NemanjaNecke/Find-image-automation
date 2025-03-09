# Google Lens Book Extractor

A command-line tool that automates [Google Lens](https://lens.google.com) to process a folder of images (typically book covers) and extract the most common candidate title from the search results. The script uses Selenium with stealth techniques to mimic human behavior while navigating Google Lens.

## Features

- **Command-Line Interface:**  
  Accepts a folder path containing images and an output filename for results.
  
- **Automated Image Processing:**  
  For each image, the script opens Google Lens, uploads the image, waits for the results, and extracts the candidate title from anchor tags.

- **Stealth Automation:**  
  Uses `selenium-stealth` to help mask automated browser behavior.

- **No External Filters:**  
  Removes previous filtering for OLX and Kupindo links, focusing solely on extracting candidate names from all available links.

## Prerequisites

- **Python 3.12+**
- **Google Chrome**
- Required Python packages (see below).

## Installation

1. **Clone the Repository:**

```
git clone https://github.com/NemanjaNecke/Find-image-automation.git
cd google-lens-book-extractor
`

2. **Create a Virtual Environment (optional but recommended):**

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3. **Install Dependencies:**


```
pip install -r requirements.txt

