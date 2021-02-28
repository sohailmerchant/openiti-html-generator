"""Create html versions of all OpenITI text files in a folder (and its subfolders).

Main function:
convert_all_files_in_folder(folder, meta_fp='metadata.csv', template_path="template/main.html")
"""

import re
import os
from bs4 import BeautifulSoup
from openiti.helper.funcs import get_all_text_files_in_folder
import shutil
import json

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
    h_regex = "(<h\d+.+?id='[^']+')"
    new_s = ""
    i = 0
    for x in re.split(h_regex, s):
        if x.startswith("<h"):
            new_s += re.sub("id='.+", "id='head{}'".format(i), x)
            i += 1
        else:
            new_s += x
    return new_s

def toc_to_ul(toc):
    """Convert the table of contents into a collapsible list

    See http://code.iamkate.com/javascript/collapsible-lists/
    """
    ul = "<div class='card-header title-heading'>فصول الكتاب</div><ul class='collapsibleList'>\n "
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


def escape(s):
    """Escape special characters in string to use it in regex search"""
    return re.sub(r"([[\]()|.*$\^])", r"\\\1", s)



def toc_tags(s, vol_no):
    """Create the tags inside table of contents for the current volume

    Args:
        s (str): OpenITI text
    """
    toc = []
##    tag = """
##                    <a class='toc-item l{0}' href='{1}.html#head{2}' onclick='goTo(); return False'>{3}</a>"""
    tag = """
                    <a class='toc-item l{0}' href='{1}.html#head{2}'>{3}</a>"""

    
    for i, r in enumerate(re.findall("### (\|+) (.*)", s)):
        level, title = r
        toc.append(tag.format(len(level), vol_no, i, title))
    return toc

def split_volumes(s):
    """Split the OpenITI text string into its volumes.

    Args:
        s (str): OpenITI text as string

    Returns:
        list (list of lists: (volume number, volume string, page numbers))
    """
    meta_header, s = re.split("#META#Header#End#?", s)
    
    vol_regex = "(PageV{}+P\w+)"
    all_volume_nos = set(re.findall("PageV([^P]+)", s))
    vols = []
    for v in sorted(list(all_volume_nos)):
        #print("Volume:", v)
        if v != "00":
            # split the pages with volume number `v` off from `s`:
            s_split = re.split(vol_regex.format(v), s)
            vol_content = "".join(s_split[:-1])
            s = s_split[-1]
            # get list of page numbers in volume:
            pages = re.findall("PageV[^P]+P(\w+)", vol_content)
            # add data to vols list:
            vols.append([v, vol_content, pages])
    # add the remainder of the text string (usually, a milestone)
    # after the last page number to the last volume:
    if s:
        vols[-1][1] += s
    
##    print("Number of volumes:", len(vols))
##    total_len = 0
##    for vol in vols:
##        print("len(vol[1]):", len(vol[1]))
##        total_len += len(vol[1])
##        print(vol[1][-100:])
##        print("---")
##    print("total length:", total_len)
    return vols    

def html_builder(s, meta, toc, template_path):
    """Build the body of the html file

    Args:
        s (str): OpenITI text as string
        meta (dict): dictionary containing the metadata of the book
        toc (str): table of contents (html string)
        template_path (str): path to the html template
    """
    s = convert_text(s)
    
##    # create right navigation panel: 
##    #right = toc_tags(s)
## 
##    with open(template_path, 'r') as html:
##        contents = html.read()
##
##        soup = BeautifulSoup(contents, 'lxml')
##
##        
##        right_div = soup.find(id='sidebar-wrapper')
##        book_main = soup.find(id='content')
##        metadata = soup.find(id='metadata-content')
##
##        for key, value in meta.items():
##
##            new_p = soup.new_tag("label")
##            value = key + ": " + value
##            new_p.append((value))                           
##            metadata.insert(0, new_p)
##        
##        soup.new_tag("div", right_div.append(BeautifulSoup(toc, 'lxml')))
##        soup.new_tag("div", book_main.insert(1, BeautifulSoup(s, 'html.parser')))
##       
##    # format main text as html:
##    
##    full_html = soup
##    return str(full_html)
    return s

def build_index_html(meta, toc, template_path, vols):
    with open(template_path, mode='r', encoding="utf-8") as html:
        contents = html.read()

    # set thisVolume variable so that js loads first volume initially:
    first_vol = vols[0][0]
    if first_vol != "01":
        v = 'var thisVolume = "{}"'
        contents = re.sub(v.format("01"), v.format(first_vol), contents)

    # provide js with a dictionary with list of page numbers in every volume:
    pages = json.dumps({v[0]: v[2] for v in vols})  # {vol_no: list_of_pages}
    contents = re.sub('"volPages"', pages, contents)

    soup = BeautifulSoup(contents, 'lxml')
    
    right_div = soup.find(id='sidebar-wrapper')
    book_main = soup.find(id='content')
    metadata = soup.find(id='metadata-content')

    for key, value in meta.items():

        new_p = soup.new_tag("label")
        value = key + ": " + value
        new_p.append((value))                           
        metadata.insert(0, new_p)
    
    soup.new_tag("div", right_div.append(BeautifulSoup(toc, 'lxml')))
    #soup.new_tag("div", book_main.insert(1, BeautifulSoup(s, 'html.parser')))
   
    # format main text as html:
    
    full_html = soup
    return str(full_html)
   

def create_json_file(html_str, pages, vols, outfp):
    print("SAVING AS", outfp)
    d = {"content": html_str, "pages": pages, "volumes": [v[0] for v in vols]}
    with open(outfp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

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

    For each text file, a folder is creted that contains
    - an index.html file that contains
      the navbar, table of contents and footer,
      and javascript that inserts the content of a volume into this structure.
    - For each volume of the text, a separate json file
      that contains the html-formatted text of the volume,
      in addition to a list of the page numbers in that volume. 

    Args:
        folder (str): path to folder containing the (subfolders with) text files
        meta_fp (str): path to the file containing the metadata
        template_path (str): path to the file that contains the html template
        outfolder (str): path to the 
    """
    # copy css, js and img folders into outfolder:
    copy_infrastructure(outfolder)

    # create index.md file that will contain the links to all texts:
    outfp = os.path.join(outfolder, "index.md")
    with open(outfp, mode="w", encoding="utf-8") as file:
        file.write("")


    for fp in get_all_text_files_in_folder(folder):
        version_uri = re.split(r"[/\\]", fp)[-1]
        print(version_uri)
        version_uri = ".".join(version_uri.split(".")[:3]) # split off extension
        book_id = version_uri.split(".")[2].split("-")[0]
        #print(book_id)
        with open(fp, encoding='utf-8') as f:
            s = f.read()
        
        # get the metadata of the book by id
        meta = get_metadata_by_id(book_id, meta_fp)

        # split the book into its volumes:
        vols = split_volumes(s)

        # build the table of contents:
        toc = []
        for vol_no, s, pages in vols:
            toc += toc_tags(s, vol_no)
        toc = toc_to_ul(toc)

        # create the folder for the volume files:
        if not os.path.exists(os.path.join(outfolder, version_uri)):
            os.makedirs(os.path.join(outfolder, version_uri))

        # create index.html file:
        index_html = build_index_html(meta, toc, template_path, vols)
        outfp = os.path.join(outfolder, version_uri, "index.html")
        create_html_file(index_html, outfp)
        
        # save the volume files:
        for vol_no, s, pages in vols:
            # convert to html and save file:
            html_str = html_builder(s, meta, toc, template_path=template_path)
            
            outfp = os.path.join(outfolder, version_uri, vol_no+".json")
            create_json_file(html_str, pages, vols, outfp)

        # add fp to index.md file:
        outfp = os.path.join(outfolder, "index.md")
        with open(outfp, mode="a", encoding="utf-8") as file:
            file.write("[{0}]({0})\n\n".format(version_uri))


def copy_infrastructure(outfolder, infra_folders=["css", "js", "img"]):
    """Copy the css, js and img folders into outfolder.

    Args:
        outfolder (str): path to the folder where text directories will be created.
    """
    for f in infra_folders:
        to_path = os.path.join(outfolder, f)
        if os.path.exists(to_path):
            shutil.rmtree(to_path)
        shutil.copytree("../"+f, to_path)

if __name__ == "__main__":
    #path = r"/mnt/c/Development Work/0400AH/data/"
    #path = r"/mnt/c/Development Work/0400AH/data/test/"
    path = r"/home/admin-kitab/Documents/OpenITI/Github_clone/0325AH/data/0310Tabari/0310Tabari.Tarikh"
    meta_fp= r'/home/admin-kitab/Documents/Projects/kitab-metadata-automation/output/OpenITI_Github_clone_metadata_light.csv'
    outfolder = r"/home/admin-kitab/Documents/Projects/Sohail/lite-reader"
    template_path= r"template/main_volumes.html"
    #path = "test"
    #meta_fp = "metadata.csv"
    #outfolder = "output2"
    convert_all_files_in_folder(path, meta_fp, template_path, outfolder)
