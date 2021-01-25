from bs4 import BeautifulSoup
base_path = 'template/'
with open(base_path + 'main.html', 'r') as f:

    contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')
    print(soup.head)
    tag = soup.find(class_='main')
    ultag = soup.new_tag('ul')
    #ultag = soup.ul
    newtag = soup.new_tag('li')
    newtag.string = 'OpenBSD'
    ultag.insert(1,newtag)
    tag.insert(1, ultag)
    print(tag.prettify())
