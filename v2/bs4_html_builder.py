"""Create html versions of all OpenITI text files in a folder (and its subfolders).

Main function:
convert_all_files_in_folder(folder, meta_fp='metadata.csv', template_path="template/main.html")
"""

import urllib.request
import re
import os
from bs4 import BeautifulSoup
from openiti.helper.funcs import get_all_text_files_in_folder

import config
import utility


def convert_text(s):
    """Convert an OpenITI text to html \
    using the `repl` list of patterns and replacements in the config.py file

    Args:
        s (str): text in OpenITI mARkdown format

    Returns:
        s (str): text with html markup
    """
    for d in config.repl: # loaded from config.py
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
    
def html_builder(s, meta, template_path):
    """Build the body of the html file

    Args:
        s (str): OpenITI text as string
        meta (dict): dictionary containing the metadata of the book
    """
    s = convert_text(s)
    
    # create right navigation panel: 
    right = toc_panel(s)
 
    with open(template_path, 'r') as html:
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

def create_html_file(html_str, outfp):
    print("SAVING AS", outfp)

    ## fix the path issue
    with open(outfp, "w", encoding="utf-8") as e:
        e.write(html_str)

def get_metadata_by_id(book_id, meta_fp):
    """Get the metadata for the book by book id

    Args:
        book_id (str): Book Id  as string
    """
    book_details = utility.get_book_metadata(book_id, meta_fp)
    #print(book_details)
    title = book_details['title_lat']
    title_ar = book_details['title_ar']
    author_date = book_details['date']
    author_ar = book_details['author_ar']
    author_eng = book_details['author_lat']
    #print(title)

    return book_details   


def convert_all_files_in_folder(folder, meta_fp='metadata.csv',
                                template_path="template/main.html", outfolder="."):
    """Convert all text files in the folder (and its subfolders) into html.

    Args:
        folder (str): path to folder containing the (subfolders with) text files
        meta_fp (str): path to the file containing the metadata
    """
    for fp in get_all_text_files_in_folder(folder):
        version_uri = re.split(r"[/\\]", fp)[-1]
        print(version_uri)
        book_id = version_uri.split(".")[2].split("-")[0]
        print(book_id)
        with open(fp, encoding='utf-8') as f:
            s = f.read()
        
        # get the metadata of the book by id
        meta = get_metadata_by_id(book_id, meta_fp)

        # convert to html and save file
        html_str = html_builder(s, meta, template_path=template_path)
        outfp = os.path.join(outfolder, version_uri+".html")
        create_html_file(html_str, outfp)

if __name__ == "__main__":
    #path = r"/mnt/c/Development Work/0400AH/data/"
    #path = r"/mnt/c/Development Work/0400AH/data/test/"
    path = "test"
    meta_fp='metadata.csv'
    template_path="template/main.html"
    outfolder = "."
    convert_all_files_in_folder(path, meta_fp, template_path, outfolder)
