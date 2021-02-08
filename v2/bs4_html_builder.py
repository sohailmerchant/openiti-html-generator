import urllib.request
import re
import os
from bs4 import BeautifulSoup
# load repl list and replace functions from config.py: 
from config import *
from utility import *

base_path = 'template/'

#path = r"/mnt/c/Development Work/0400AH/data/"
path = r"/mnt/c/Development Work/0400AH/data/test/"
book_id = ''

def select_files(path):

    for root, dirs, files in os.walk(path):
        print(root)
     
        for name in files:
            
            if re.search('^\d{4}\w+\.\w+\.\w+-[a-z]{3}\d{1}(\.(mARkdown|inProgress|completed))?$',name):
            
                book_name = name
                print(book_name)
                book_id = name.split(".")[2].split("-")[0]
                print(book_id)
                with open(root+'/'+name,encoding='utf-8') as f:
                    data = f.read()

                def convert_text(s):
                        """Convert an OpenITI text to html \
                        using the `repl` list of patterns and replacements in the config.py file

                        Args:
                            s (str): text in OpenITI mARkdown format

                        Returns:
                            s (str): text with html markup
                        """
                        for d in repl: # loaded from config.py
                            if "flags" in d:
                                s = re.sub(d["ptrn"], d["repl"], s, flags=d["flags"])
                            else:
                                s = re.sub(d["ptrn"], d["repl"], s)
                        return s

                def toc_to_ul(toc):
                    """Convert the table of contents into a collapsible list

                    See http://code.iamkate.com/javascript/collapsible-lists/
                    """
                    ul = "<div class='card-header title-heading'>عنوان الفصل</div><ul class='collapsibleList'>\n "
                    level = 1
                    for a in toc:
                        lev = int(re.findall("l(\d+)", a)[0])
                        if lev > level:
                            while lev > level:
                                ul += "{}<ul class='collapsibleList'>\n".format(" "*level*4)
                                level += 1
                        elif lev < level:
                            while lev < level:
                                ul += "\n{}</li>".format(" "*level*4)
                                level -= 1
                                ul += "\n{}</ul>\n".format(" "*level*4)

                        ul += "{0}<li class='collapsibleListClosed'>{1}\n".format(" "*level*4, a)
                    while level > 0:
                        ul += "\n{}</li>".format(" "*level*4)
                        level -= 1
                        ul += "\n{}</ul>\n".format(" "*level*4)
                    
                    return ul

                def toc_panel(html):
                    """Create the table of contents panel

                    Args:
                        html (str): OpenITI text converted to html
                    """
                    toc = []
                    for level, title in re.findall("<h\d+ .+?l(\d+).+?id='([^']+)", html):
                        tag = """
                                    <a class='toc-item l{0}' href='#{1}'>{1}</a>"""
                        toc.append(tag.format(level, title))
                    toc = toc_to_ul(toc)
                    
                    return toc
                    
                def html_builder(s, meta):
                    
                    
                    """Build the body of the html file

                    Args:
                        s (str): OpenITI text as string
                        uri (str): OpenITI version URI of the text
                    """
                    s = convert_text(s)
                    
                    # create right navigation panel: 
                    right = toc_panel(s)
                 
                    with open(base_path + 'main.html', 'r') as html:

                        contents = html.read()

                        soup = BeautifulSoup(contents, 'lxml')

                        
                        right_div = soup.find(id='sidebar-wrapper')
                        book_main = soup.find(id='content')
                        metadata = soup.find(id='metadata-content')

                        for key, value in meta.items():

                            new_p = soup.new_tag("label")
                            value = key + ": " + value
                            new_p.append((value))                           
                            metadata.insert(0, new_p)
                        
                        soup.new_tag("div", right_div.append(BeautifulSoup(right, 'lxml')))
                        soup.new_tag("div", book_main.insert(1, BeautifulSoup(s, 'html.parser')))

                        
                       
                    # format main text as html:
                    
                    full_html = soup
                    
                    
                    

                    return str(full_html)

                def create_html_file(html_str):
                    print("SAVING AS", book_name + ".html")

                    ## fix the path issue
                    with open(book_name + ".html", "w", encoding="utf-8") as e:
                        e.write(html_str)

                def get_metadata_by_id(book_id):
                    """Get the metadata for the book by book id

                    Args:
                        book_id (str): Book Id  as string
                    """
                    book_details = get_book_metadata(book_id)
                    #title = book_details['title_lat']
                    title_ar = book_details['title_ar']
                    author_date = book_details['date']
                    author_ar = book_details['author_ar']
                    author_eng = book_details['author_lat']
                    #print(title)

                    return book_details

                s = data
                
                # get the metadata of the book by id
                meta = get_metadata_by_id(book_id)

                html_str = html_builder(s, meta)
                create_html_file(html_str)


select_files(path)