# ghost_writer
get blog entries, create pdf, interact with gen-ai to get better results. 

## extract blogs
__source file__: exrtract_blogs.py

my first attempt to extract blog entries and create a word file. 

### purpose
the script processes atom-formatted xml site feeds exported from blogger's "back up content" feature. it extracts blog entries matching specific criteria and formats them into a word document with headings, text, and images.

### functionality
- input: the xml file is parsed to extract <entry> elements, filtered by blog id and title.
- content processing: beautifulsoup parses html content to extract headings, paragraphs, and images.
- output: the script uses python-docx to create a word document, organizing each entry with titles, metadata, and content.

### known limitations
- it does not extract google maps embedded as iframes.
- it does not handle images properly, leading to incomplete extraction.

discarded due to limiations. 

## exrtract blog entries
__source file__: exrtract_blog_entries.py

