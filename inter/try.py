import fitz

try:
	doc = fitz.open('a.pdf')
except Exception as e:
        print({"error": str(e)})
        exit(1)
num_pages = doc.page_count
text = ''
for i in range(num_pages):
    page = doc.load_page(i)
    text += page.get_text()
print(text)