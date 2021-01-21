import urllib.request
import re
from bs4 import BeautifulSoup
# load repl list and replace functions from config.py: 
from config import *


#book_url= "https://raw.githubusercontent.com/OpenITI/0300AH/master/data/0281IbnAbiDunya/0281IbnAbiDunya.TawaducWaKhumul/0281IbnAbiDunya.TawaducWaKhumul.JK000002-ara1.mARkdown"
#book_url = "https://raw.githubusercontent.com/OpenITI/0325AH/master/data/0310Tabari/0310Tabari.MuntakhabMinDhayl/0310Tabari.MuntakhabMinDhayl.Shamela0001133-ara1.completed"
#book_url = "https://raw.githubusercontent.com/OpenITI/0300AH/master/data/0279Baladhuri/0279Baladhuri.AnsabAshraf/0279Baladhuri.AnsabAshraf.Shamela0009773-ara1.completed"
book_url = "https://raw.githubusercontent.com/OpenITI/0325AH/master/data/0325IbnIshaqWashsha/0325IbnIshaqWashsha.Muwashsha/0325IbnIshaqWashsha.Muwashsha.Shamela0026102-ara1.completed"
book_name = book_url.split(r'/')[-1]

data = urllib.request.urlopen(book_url)


def html_open():

    html_opening_tag = """<html dir="rtl" lang="ar">
    <head>

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.rtl.min.css">
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Amiri&display=swap" rel="stylesheet">
     
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        
        <meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="css/style.css"  />
        <script type="text/javascript" src="js/CollapsibleLists.js"></script>
        
    </head>
    <body>
        <div class="container-fluid h-100">
        	<!-- Navigation -->
	<nav class="navbar navbar-default">
		<div class="container-fluid">
		  <div class="navbar-header">
			
			<a class="navbar-brand" href="http://www.kitab-project.org" target="_blank" style="margin-top:5px">
				<img src="http://web.kitab-project.org/wp-content/uploads/2017/07/logo-small-2.png" width="80px"/></a>
		  </div>
		  
		</div>
	  </nav>
        """

    return html_opening_tag

def html_close():
    html_closing_tag = """</div></div></div></body>
        <script type="text/javascript">
            CollapsibleLists.apply();
            console.log("Applied");
        </script>
    </html>"""
    return html_closing_tag

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
    ul = "<div style='text-align:center!important'>Book Headings</div><ul class='collapsibleList'>\n "
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
    toc = """
                <div class='col-md-4' id='right'>
                    <div class='right-panel shadow bg-white rounded' style='text-align: right;direction:rtl;'>
                        {}
                    </div>
                </div>
    """.format(toc)
    return toc

def html_builder(s, uri):
    """Build the body of the html file

    Args:
        s (str): OpenITI text as string
        uri (str): OpenITI version URI of the text
    """
    s = convert_text(s)
    
    # create right navigation panel: 
    right = toc_panel(s)

    # format main text as html:
    header = """
    <div class='row p-30'>
        <div class='col-md-12'>
            <div class="row top-heading-panel content-outer-spacing">
	        <div class="col-md-12">
		    <h3>
		        {}
		    </h3>
            <span></span>
		</div>
		<div class="col-md-12" id="meta">
		</div>
	    </div> 
            
    """.format(".".join(uri.split(".")[:2]))


    left = """<div class="row">
                <div class="col-md-8" id="left">
                    <div class='shadow p-3 mb-5 bg-white rounded content-outer-spacing'>
                    
                        {}
                    </div>
                </div>
                
    """.format(s)
    
    footer="""
                <div class="row" id='footer'><div class="col-md-12">
                    This file is produced based on the data available on the KITAB/OpenITI Corpus.  The <a class="" href="http://www.kitab-project.org" target="_blank">KITAB Project</a> is funded by ERC. All right reserved as per Apache Licence... 
		</div>
	    </div>
    """

    full_html = html_open()
    full_html += header
    full_html += right
    full_html += left
    full_html += footer
    full_html += html_close()

    return full_html

def create_html_file(html_str):
    print("SAVING AS", book_name + ".html")
    with open(book_name + ".html", "w", encoding="utf-8") as e:
        #e.write(html_open())
        e.write(html_str)
        #e.write(html_close())

def get_text_insights(s):
    """Get the insights about the text including counts of various tags

    Args:
        s (str): OpenITI text as string
    """
    q = len(re.findall(r'@QB@\s?(.*?)@QE@\s?',s,flags=re.DOTALL))
    m = len(re.findall(r'(ms\d+)',s,flags=re.DOTALL))
    print("No. of Quranic Reference: {} No of Milestones {}".format(q, m))

# test = """\
# ### |EDITOR|
# # المنتخب من كتاب ذيل المذيل من تاريخ الصحابة والتابعيه
# # تصنيف أبى جعفر محمد بن جرير الطبري
# # (1358 ه - 1939 م)
# # منشورات مؤسسة الأعلمي للمطبوعات، بيروت - لبنان، ص. ب. 7120
# # 
# ### $ first ms0002 PageV01P001 title
# # بسم الله الرحمن الرحيم
# # hemistich 1 %~% hemistich 2
# # قال أبو جعفر ms1234 محمد بن جرير بن يزيد الطبري في كتاب ذيل المذيل من تأريخ
# ~~الصحابة والتابعين: @QB@ وكان فيما ذكر
# رجلا ليس @QE@ وكان فيما ذكر رجلا ليس"""

# print(convert_text(test))
# input()


s = data.read().decode('utf-8')
get_text_insights(s)
html_str = html_builder(s, book_name)
create_html_file(html_str)
