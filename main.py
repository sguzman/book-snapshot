import brotli
import bs4
import json
import sys

snapshot = './snapshot/books.brotli' if len(sys.argv) is 1 else sys.argv[1]
file = open(snapshot, 'rb').read()
string = brotli.decompress(file)
books = string.split(b'</html>')[:-1]


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):].replace('/', '')
    return text


objects = []
for book in books:
    new_book = '%s</html>' % book
    doc = bs4.BeautifulSoup(new_book, "html.parser")

    title = doc.find('h1', class_='post-title').get_text()
    img = doc.find('div', class_='book-cover').img['src']
    p = doc.find('div', class_='entry-inner').get_text()
    cats = doc.find('p', class_='post-btm-cats').findAll('a')
    categories = [a.get_text() for a in cats]

    details = doc.find('div', class_='book-details').ul
    keys = details.findAll('span')
    vals = details.findAll('li')
    detailsDict = {}
    for i in range(len(keys)):
        keyStr = keys[i].get_text()
        valStr = vals[i].get_text()

        new_str = remove_prefix(valStr, keyStr)
        detailsDict[keyStr[:-1].lower()] = new_str

    detailsDict['title'] = title
    detailsDict['img'] = img
    detailsDict['desc'] = p
    detailsDict['categories'] = categories

    objects.append(detailsDict)

print(json.dumps(objects, sort_keys=True, indent=4))
