import urllib.request
import re
import os
from bs4 import BeautifulSoup
# load repl list and replace functions from config.py: 
from config import *
from utility import *

#path = r"/mnt/c/Development Work/0400AH/data/"
path = r"/mnt/c/Development Work/0400AH/data/test/"
book_id = ''
def select_files(path):

    for root, dirs, files in os.walk(path):
     
        for name in files:
            #book_url= "https://raw.githubusercontent.com/OpenITI/0300AH/master/data/0281IbnAbiDunya/0281IbnAbiDunya.TawaducWaKhumul/0281IbnAbiDunya.TawaducWaKhumul.JK000002-ara1.mARkdown"
            #book_url = "https://raw.githubusercontent.com/OpenITI/0325AH/master/data/0310Tabari/0310Tabari.MuntakhabMinDhayl/0310Tabari.MuntakhabMinDhayl.Shamela0001133-ara1.completed"
            #book_url = "https://raw.githubusercontent.com/OpenITI/0300AH/master/data/0279Baladhuri/0279Baladhuri.AnsabAshraf/0279Baladhuri.AnsabAshraf.Shamela0009773-ara1.completed"
            #book_url = "https://raw.githubusercontent.com/OpenITI/0325AH/master/data/0325IbnIshaqWashsha/0325IbnIshaqWashsha.Muwashsha/0325IbnIshaqWashsha.Muwashsha.Shamela0026102-ara1.completed"
            #book_url = r"C:\Development Work\openiti-html-generator\README.md"
            #
            #book_name = '0977KhatibShirbini.Iqnac.Shamela0006121-ara1'
                
            if not (name.endswith('.yml') or name.endswith('.md')):
                book_name = name
                print(book_name)
                book_id = name.split(".")[2].split("-")[0]
                print(book_id)
                with open(root+'/'+name,encoding='utf-8') as f:
                    data = f.read()
                    #data = urllib.request.urlopen(book_url)

                    def html_open():

                        html_opening_tag = """<html dir="rtl" lang="ar">
                        <head>

                            <meta charset="utf-8">

                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                            
                            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
                            <link rel="preconnect" href="https://fonts.gstatic.com">
                            <link href="https://fonts.googleapis.com/css2?family=Amiri&display=swap" rel="stylesheet">
                        
                            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>

                            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
                            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">

                            
                            <link rel="stylesheet" type="text/css" href="../css/style.css"  />
                            <script type="text/javascript" src="../js/CollapsibleLists.js"></script>
                        
                            
                        </head>
                        <body>
                            <nav class="navbar navbar-light bg-light">
                            <div class="container-fluid">
                                <a class="navbar-brand" href="http://www.kitab-project.org" target="_blank">
                                <img src="../img/kitab-logo.png" width="60px"/></a>
                                
                                <a class="nav-link" aria-current="page" href="https://sohailmerchant.github.io/lite-reader/index.html">Book Index</a>
                               
                            </div>
                            </nav>
         
                        
                            """

                        return html_opening_tag

                    def html_close():
                        html_closing_tag = """</div></div></div>
                       
                        </body>
                            <script type="text/javascript">
                                CollapsibleLists.apply();
                                console.log("Applied");
                                        
                            $(document).ready(function () {
                              $(window).scroll(function () {
                                if ($(this).scrollTop() > 50) {
                                    $('#back-to-top').fadeIn();
                                } else {
                                    $('#back-to-top').fadeOut();
                                }
                            });
                            // scroll body to 0px on click
                            $('#back-to-top').click(function () {
                                $('body,html').animate({
                                    scrollTop: 0
                                }, 400);
                                return false;
                            });
                                function toggleSidebar(side) {
                                    if (side !== "left" && side !== "right") {
                                        return false;
                                    }
                                    var left = $("#sidebar-left"),
                                        right = $("#sidebar-right"),
                                        content = $("#content"),
                                        openSidebarsCount = 0,
                                        contentClass = "";
                                    
                                    // toggle sidebar
                                    if (side === "left") {
                                        left.toggleClass("collapsed");
                                    } else if (side === "right") {
                                        right.toggleClass("collapsed");
                                    }
                                    
                                    // determine number of open sidebars
                                    if (!left.hasClass("collapsed")) {
                                        openSidebarsCount += 1;
                                    }
                                    
                                    if (!right.hasClass("collapsed")) {
                                        openSidebarsCount += 1;
                                    }
                                    
                                    // determine appropriate content class
                                    if (openSidebarsCount === 0) {
                                        contentClass = "col-md-12";
                                    } else if (openSidebarsCount === 1) {
                                        contentClass = "col-md-9";
                                    } else {
                                        contentClass = "col-md-6";
                                    }
                                    
                                    // apply class to content
                                    content.removeClass("col-md-12 col-md-9 col-md-6")
                                        .addClass(contentClass);
                                }
                                $(".toggle-sidebar-left").click(function () {
                                    toggleSidebar("left");
                                    
                                    return false;
                                });
                                $(".toggle-sidebar-right").click(function () {
                                    toggleSidebar("right");
                                    
                                    return false;
                                });
                            });

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
                        ul = "<div class='card-header'>عنوان الفصل</div><ul class='collapsibleList'>\n "
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
                        toc = """<div class="row " id="row-main">
                                    <div class='col-md-3 sidebar' id='sidebar-right'>
                                        <div class='right-panel shadow bg-white rounded sticky-top'>
                                            {}
                                        </div>
                                    </div>
                        """.format(toc)

                        return toc

                    def html_builder(s, uri,bi, book_id):
                        book_details = get_book_metadata(book_id)
                        
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
                                <div class="col-md-12 h-100">
                                <h4>
                                    {}
                                </h4>
                                </div>
                                </div>
                            </div>
                            <div class="col-md-12" id="meta">
                            </div>
                            </div> 
                                
                        """.format(book_details['title_lat'] + " by " + book_details['author_lat'])
                       
                        #.format(".".join(uri.split(".")[:2]))

                        main = """
                                    <div class="col-md-6" id="content">
                                    <div class="card-header sticky-top">
                                    <div class="row">
                                    
                                     <div class="col-md-3">
                                        <i class="bi bi-arrows-angle-expand toggle-sidebar-left toggle-sidebar-right">
                                        </i>
                                        </div>
                                        <div class="col-md-9" style='text-align:left'>
                                        <i id="back-to-top" class="bi bi-arrow-bar-up">
                                        </i>
                                        </div>
                                        
                                    
                                    </div>
                                    </div>
                                        <div class='shadow p-3 mb-5 bg-white rounded'>
                                        
                                            {}

                                        </div>
                                </div>
                                    
                        """.format(s)

                        left = """
                        
                        <div class='col-md-3 sidebar' id='sidebar-left'> 
                        <div class='left-panel shadow bg-white rounded sticky-top'>
                        <div class='card-header'>
                                        رؤى الكتاب
                                        </div>
                                        <div class="card-body">
    

                                        {}
                                          </div>
                                        </div>
                                        </div>
                        </div>""".format(bi + "<p>" 'Word Count: '+ book_details['tok_length'].strip() + "</p>")
                        
                        footer="""
                                    <div class="row" id='footer'><div class="col-md-12">
                                        KITAB project has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (Grant agreement No. ) 
                            </div>
                            </div>
                        """

                        full_html = html_open()
                        full_html += header
                        full_html += right
                        full_html += main
                        full_html += left
                        full_html += footer
                        full_html += html_close()

                        return full_html

                    def create_html_file(html_str):
                        print("SAVING AS", book_name + ".html")
                        with open("output/"+ book_name + ".html", "w", encoding="utf-8") as e:
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
                        #print("No. of Quranic Reference: {} No of Milestones {}".format(q, m))
                        return "<p>Quranic Reference: {}</p> <p>Milestones: {} </p>".format(q, m)

                   
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


                    #s = data.read().decode('utf-8')
                    
                s = data
                bi = get_text_insights(s)
                html_str = html_builder(s, book_name, bi, book_id)
                create_html_file(html_str)

select_files(path)