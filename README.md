Below is a sample **README.md** that implements the recommended improvements and consolidates all details in a clean, user-friendly structure. Feel free to customize the text, headings, and order of sections as you see fit.

---

# Ghost Writer

> **A Python utility that fetches and formats Blogger posts into Word and PDF documents, complete with images, captions, and Google Maps screenshots.**

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Logging](#logging)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)
9. [Contributing](#contributing)

---

## Overview

**Ghost Writer** uses the Blogger API to retrieve posts from a specified Blogger blog, parse their HTML contents (including images, lists, headings, and Google Maps embeds), then exports them into nicely formatted Word (`.docx`) documents. It can further convert these `.docx` files into PDF. The project relies on Selenium to capture screenshots for any embedded Google Maps.

---

## Key Features

- **Automated Post Retrieval** – Pulls blog posts via the Blogger API.
- **HTML Parsing** – Handles headings, paragraphs, lists, images, and other elements.
- **Google Maps Screenshot** – Uses Selenium to fetch and insert maps as images.
- **Word Document Generation** – Provides consistently styled `.docx` exports (with optional chunking).
- **PDF Conversion** – Converts generated `.docx` documents into `.pdf`.
- **Custom Styling** – Applies an Aptos font and spacing for a professional look.
- **Detailed Logging** – Offers comprehensive logs to help troubleshoot any issues.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/kkhegde/ghost_writer.git
cd ghost_writer
```

### 2. (Optional) Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note:** This includes Selenium, `webdriver_manager`, `google-api-python-client`, and other libraries required by the script.

### 4. Ensure Chrome is Installed
Ghost Writer uses **Chrome** and its corresponding driver. If you encounter driver errors, try updating Chrome or installing the exact driver version manually.

---

## Configuration

1. **Create a `config.json` File**  
   In the project root, create a file named `config.json` with the following content:
   ```json
   {
     "BLOGGER_API_KEY": "YOUR_GOOGLE_BLOGGER_API_KEY",
     "TRAVEL_BLOG_ID": "YOUR_BLOGGER_BLOG_ID"
   }
   ```
   - `BLOGGER_API_KEY`: Your Google API key (ensure Blogger API is enabled in the Google Cloud Console).
   - `TRAVEL_BLOG_ID`: The Blogger ID of the blog you want to extract posts from.

2. **.env or Additional Secrets** (Optional)  
   If you prefer using a `.env` file for secrets, ensure you also update `.gitignore` to prevent committing sensitive information.

3. **Adjust Script Parameters**  
   In `extract_blog_entries.py` (or in your environment), you can change:
   - `blog_post_list` – Path where URLs of blog posts are saved/loaded.
   - `output_docx_file` – Path for the final Word document.
   - `output_pdf_file` – Path for the final PDF output.
   - `output_docx_path` – Directory for multi-chunk docx files.
   - `chunk_size` – Number of posts to include per docx file when chunking.

---

## Usage

Running the script **in its simplest form**:
```bash
python extract_blog_entries.py
```

By default, the script:
1. Fetches all blog URLs from your Blogger site (using `TRAVEL_BLOG_ID` and `BLOGGER_API_KEY`).
2. Logs the collected URLs in a text file (as defined by `blog_post_list`).
3. (Optionally) Creates `.docx` and `.pdf` versions of all posts (if the relevant lines are uncommented in `__main__`).

If you want to **enable or disable specific actions**, open `extract_blog_entries.py` and look at the `__main__` section. You’ll see lines like:

```python
# log_execution("create_travel_blog_docx",
#               extractor.create_travel_blog_docx,
#               extractor.output_docx_file,
#               extractor.blog_post_list)

# log_execution("convert_docx_to_pdf",
#               extractor.convert_docx_to_pdf,
#               extractor.output_docx_file,
#               extractor.output_pdf_file)
```

Uncomment the desired lines to:
- **Create DOCX**: Generate a single Word file containing all extracted posts.
- **Convert to PDF**: Convert the generated `.docx` to `.pdf`.
- **Create DOCX in chunks**: If you have many posts, you can split them into multiple files for easier management.

---

## Logging

Ghost Writer logs each step of the process to:
- **Console** – displays progress and potential errors in real time.
- **`travel_blog_extractor.log`** – located in the project directory, capturing the same log messages.

Check this file (or your console output) for detailed information if you encounter issues.

---

## Troubleshooting

- **ChromeDriver / WebDriver Manager Mismatch**  
  If you see errors about ChromeDriver not matching your installed Chrome version, update your local Chrome or specify a driver version in `webdriver_manager`. You can also manually install ChromeDriver for your version of Chrome.
  
- **API Key or Permission Errors**  
  Make sure your Google API key is valid, the Blogger API is enabled, and you used the correct Blogger blog ID. Double-check `config.json` or `.env` settings.
  
- **Slow or Blocked Requests**  
  Sometimes rendering a blog post or taking a screenshot might take longer. Increase `page_load_wait` or `render_pause` in the constructor to give more time.

---

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](LICENSE) license.  
You may use, share, and adapt this code for **non-commercial purposes**, provided you give appropriate credit. For more details, refer to the [LICENSE](./LICENSE).

---

## Contributing

Contributions are welcome! Please follow these steps:
1. **Fork** this repository.
2. **Create a branch** for your feature or bug fix (`git checkout -b feature/my-new-feature`).
3. **Commit** your changes (`git commit -am 'Add some feature'`).
4. **Push** to your branch (`git push origin feature/my-new-feature`).
5. **Open** a Pull Request describing your changes.

If you find bugs or have feature requests, please open an issue. We appreciate your feedback and contributions!

---

*Happy extracting! If you have questions or run into any problems, feel free to open an [issue](https://github.com/kkhegde/ghost_writer/issues) in this repository.*