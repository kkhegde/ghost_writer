# Blog Extractor

A Python utility that extracts blog posts from Blogger blogs and converts them into formatted Word (DOCX) and PDF documents. This tool preserves formatting, handles lists, embeds images, and captures Google Maps as screenshots.

## Features

- Retrieves blog posts using the Blogger API
- Preserves text formatting, headings, and paragraph styles
- Handles nested lists (both ordered and unordered)
- Embeds images with captions
- Captures Google Maps embeds as screenshots
- Supports custom font styling (Aptos)
- Creates both DOCX and PDF outputs
- Offers single file or chunked output options
- Comprehensive logging

## Requirements

- Python 3.6+
- Google Blogger API key
- Chrome WebDriver (for capturing maps)

## Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/blog-extractor.git
cd blog-extractor
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Create a `config.json` file with your API credentials
```json
{
  "BLOGGER_API_KEY": "your_blogger_api_key",
  "BLOG_ID": "your_blog_id"
}
```

## Usage

Run the main script:
```bash
python extract_blog_entries.py
```

By default, the script will:
1. Retrieve blog post URLs from your Blogger blog
2. Save the URLs to a text file
3. Generate DOCXs and PDFs as specified in your configuration

## Configuration Options

Create an instance of `BlogExtractor` with these customizable parameters:

```python
extractor = BlogExtractor(
    blog_post_list="./output/blog_post_urls.txt",
    page_load_wait=30,
    web_driver_wait=30,
    render_pause=4,
    output_docx_file="./output/blog_posts.docx",
    output_pdf_file="./output/blog_posts.pdf",
    output_docx_path="./output",
    file_name_starts_with="blog_posts_",
    chunk_size=1
)
```

| Parameter | Description |
|-----------|-------------|
| `blog_post_list` | Path to save/load blog post URLs |
| `page_load_wait` | Seconds to wait for page loading |
| `web_driver_wait` | Seconds to wait for WebDriver elements |
| `render_pause` | Seconds to pause for rendering |
| `output_docx_file` | Path for the output DOCX file |
| `output_pdf_file` | Path for the output PDF file |
| `output_docx_path` | Directory for output files |
| `file_name_starts_with` | Prefix for chunked output files |
| `chunk_size` | Number of blog posts per file when chunking |

## Functions

The extractor provides these main functions:

- `get_blog_urls()`: Retrieves blog post URLs using Blogger API
- `create_blog_docx()`: Creates a single DOCX with all blog posts
- `create_blog_docx_split()`: Creates multiple DOCXs with chunked blog posts
- `convert_docx_to_pdf()`: Converts a single DOCX to PDF
- `convert_docx_to_pdf_multi()`: Converts multiple DOCXs to PDFs

## Output Format

The generated documents include:
- Blog post titles as headings
- Formatted text with proper spacing
- Lists with proper indentation and bullet/number styles
- Images with captions
- Google Maps screenshots
- Consistent Aptos font throughout

## Customizing Output

You can modify the script to customize:
- Font styles and sizes
- Image dimensions
- Paragraph spacing
- Heading levels
- Page layouts

## Logging

The script logs detailed information about each processing step to:
- Console output
- `blog_extractor.log` file

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0) - see the [LICENSE](LICENSE) file for details.

This means you can freely use, share, and adapt this code for non-commercial purposes, as long as you provide attribution to the original author.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.