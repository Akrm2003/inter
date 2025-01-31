import fitz

doc = fitz.open('sample.pdf')
num_pages = doc.page_count
text = ''
for i in range(num_pages):
    page = doc.load_page(page_num)
    text += page.get_text()