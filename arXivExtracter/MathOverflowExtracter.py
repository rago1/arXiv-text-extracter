import bs4 as BS
#Requires lxml

r = open('/Users/paolo/Downloads/MathOverflow Corpus/Raw/posts-2013-05.xml', 'r')
xml=r.read()
r.close()
soup = BS.BeautifulSoup(xml, 'xml')

list_ = []

for item in soup.findAll('row'):
    list_.append(item.get('Body'))

print list_[100001]
