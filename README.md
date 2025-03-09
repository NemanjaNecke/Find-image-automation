# Google Lens Book Extractor

A command-line tool that automates [Google Lens](https://lens.google.com) to process a folder of images (typically book covers) and extract the most common candidate title from the search results. The script uses Selenium with stealth techniques to mimic human behavior while navigating Google Lens.

## Features

- **Command-Line Interface:**  
  Accepts a folder path containing images and an output filename for results.
  
- **Automated Image Processing:**  
  For each image, the script opens Google Lens, uploads the image, waits for the results, and extracts the candidate title from anchor tags.

- **Stealth Automation:**  
  Uses `selenium-stealth` to help mask automated browser behavior.


## Prerequisites

- **Python 3.12+**
- **Google Chrome**
- Required Python packages (see below).

## Installation

1. **Clone the Repository:**

```
git clone https://github.com/NemanjaNecke/Find-image-automation.git
cd Find-image-automation
```

2. **Create a Virtual Environment:**

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies:**


```
pip install -r requirements.txt
```


## Usage

>Run the script from the command line, providing the path to the folder containing your images and the name of the output file where the results will be saved:

`python google_lens_book_extractor.py /path/to/images output_results.txt`

**Example**

```
python google_lens_book_extractor.py ~/Downloads/BookCovers results.txt
```

This command will process all image files in the ~/Downloads/BookCovers folder and save the output to results.txt.

## How It Works

- Launching Google Lens:
  - The script navigates to Google Lens using Selenium.

- Image Upload:
   
  - It uploads each image to Google Lens by clicking the (upload file) button.

- Result Extraction:
   - Once the results load, it scans all the links on the page, extracts visible text from each, and determines the most common candidate title along with one corresponding link.

 - Output:
   - The results are saved in a text file where each line contains the image filename, the extracted candidate title, and the link.
