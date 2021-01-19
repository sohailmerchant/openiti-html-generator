import urllib.request
import re
from bs4 import BeautifulSoup

book_url= "https://raw.githubusercontent.com/OpenITI/0450AH/master/data/0428IbnSina/0428IbnSina.Shifa/0428IbnSina.Shifa.GRAR000034-ara1.completed"
#book_url = "https://raw.githubusercontent.com/OpenITI/0325AH/master/data/0310Tabari/0310Tabari.MuntakhabMinDhayl/0310Tabari.MuntakhabMinDhayl.Shamela0001133-ara1.completed"
#book_url = "https://raw.githubusercontent.com/OpenITI/0300AH/master/data/0279Baladhuri/0279Baladhuri.AnsabAshraf/0279Baladhuri.AnsabAshraf.Shamela0009773-ara1.completed"
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
        <style>
            .container{
                border:0px solid #d3ded3; 
                text-align:right;
            }

            body{
                font-family: 'Amiri', serif!important;
                font-size: 1.2rem;
            }
            html, body {
              height: 100%;
            }
            .quran{
                color:red;
            }
            .isnad{
                color:yellow;
            }
            .EDITOR{
                color:grey;
            }
            .PARATEXT{
                color:grey;
            }
            .content-outer-spacing{
                
                margin-bottom: 30px;
                padding-left: 50px!important;
                padding-right: 50px!important;
                text-align: right!important;
                 direction:rtl;

            }
            .pageno{

                font-size: 0.7rem;
                text-decoration:none;
            
            }
            .pageno-container{

                text-align:center;
            }
            .l1{

                color: #85144b;
            }

            .l2{

                color: #3D9970;
                margin-right: 10px;
            }

            .l3{
                margin-right: 20px;
                color: #39CCCC;
            }


            .dropdown-item {
                white-space: normal;
                
                border-bottom: 1px solid #d3d3d3;
            }

            .dropdown{
                text-align:left;
                width:auto;
                position:fixed;
                z-index:999;
            }
            .dropdown-menu {
                max-height:90vh;
                overflow-y:auto;
                overflow-x:hidden;
                
            }
            select, option { width: __; }

            p{
                text-indent: 10px;
            }
            .hemistich-1 {
                padding-right: 30px;
            }
            .hemistich-2 {
                padding-right: 20px;
            }

          .p-30{

              padding:30px;
          }
            
            #right {
                    
            direction:ltr; 
            overflow:auto; 
        }

        .top-heading-panel{       

                direction: rtl;
                background-color: #fafafa;
        }
        #footer{
        text-align: center;
        direction: ltr ;
        background-color: #fafafa;
        }

        </style>
        
    </head>
    <body>
        <div class="container-fluid h-100">
        """

    return html_opening_tag


def html_close():
    html_closing_tag = "</div></div></div></body></html>"
    return html_closing_tag


def convert_text(s):
    def format_section_title(m):
        pipes = m.group(1)
        title = m.group(2)
        title_link = re.sub(r"\( *([^\(]*) *\)", r"\1", title).strip() # remove parenthesis from title
        #title_link = re.sub(r"""<span id='ms\d+'></span>""", "", title_link)
        title_link = re.sub(" *<.+> *", " ", title_link) # remove all tags within title
        if "$" in pipes:
            return "<h{0} class='dic-item l{0}' id='{1}'>{2}</h{0}>\n".format(3, title_link, title)
        else:
            return "<h{0} class='l{0}' id='{1}'>{2}</h{0}>\n".format(len(pipes), title_link, title)


    # remove superfluous characters:
    s = re.sub(r'~~', "", s)
    s = re.sub("# Page", "Page", s)

    # remove header: 
    s = re.sub("######OpenITI#.+?#META#Header#End#[\r\n]+(?:PageV0+P0+[\r\n]+)?", "\n", s, flags=re.DOTALL)
    
    # tag milestones:
    ms_patttern = r'(ms\d+)'
    s = re.sub(ms_patttern, r"<span id='\1'></span>", s, flags=re.DOTALL)

    # tag poetry:
    poetry_regex = r"[\r\n]+# (.*)%~%(.*)"
    repl = r"\n<p class='poetry'><span class='hemistich-1'>\1</span><span class='hemistich-2'>\2</span></p>\n"
    s = re.sub(poetry_regex, repl, s)

    # tag paragraphs: 
    para_regex = r"[\r\n]+# (.+?)(?=[\r\n]+#|\Z|[\r\n]*<p)"
    s = re.sub(para_regex, r"\n<p>\n\1\n</p>\n", s, flags=re.DOTALL)

    # page numbers:
    page_regex = r'PageV([^P]+)P(\w+)' # in some cases this is not a number
    page_div = r"<div class='pageno-container'><a class='pageno' href='#'> Vol. \1, p. \2</a></div>"
    s = re.sub(page_regex, page_div, s)
    
    s = re.sub(r"### \|([A-Z]+)\|\s+(.*?)(?=###)",
               r"<div class='\1'>\n\2</div>\n",
               s, flags=re.DOTALL)

    # section titles: 
    s = re.sub("### ([\$\|]+) (.*)", format_section_title, s)

    # Qur'an quotes:
    quran_regex = r'@QB@\s?(.*?)@QE@\s?' # consider using "[^@]" instead of "."
    s = re.sub(quran_regex, r"<span class='quran'>\1</span>", s, flags=re.DOTALL)

    # isnads:
    isnad_regex = r'@Auto_ISB@\s(W*.+)\s@Auto_ISE@' # is the W in this regex correct?
    s = re.sub(isnad_regex, r"<span class='isnad'>\1</span>", s, flags=re.DOTALL)


    return str(s)
    #return s


def html_builder(data):
    full_html = ""
    s = data.read().decode('utf-8')

    # format main text as html:
    body = """ <div class='row p-30'>
        <div class='col-md-12'>
        	<div class="row top-heading-panel content-outer-spacing">
				<div class="col-md-12">
					<h3>
						Title of the Book
					</h3>
				</div>
			</div> 
            <div class="row">
            """

    left = """
             
            <div class="col-md-8">
            <div class='shadow p-3 mb-5 bg-white rounded content-outer-spacing'>
    """
    left += convert_text(s) + "</div></div>"

    # create right navigation panel: 
    right = """
    <div class='col-md-4' id='right'>
    <div class='right-panel shadow p-3 mb-5 bg-white rounded content-outer-spacing h-100'>
       
    """
    for level, title in re.findall("<h\d+ .+?l(\d+).+?id='([^']+)", left):
        right += " <a class='dropdown-item l{0}' href='#{1}'>{1}</a>\n".format(level, title)
    right += """
        </div></div>
    """
    
   


   

    ms = left.split(r'ms')
    # print(len(ms)-1)
    # print(ms)
    
    full_html += body
    full_html += right
    full_html += left
    
    
    footer="""<div class="row" id='footer'><div class="col-md-12">
        This file is produced based on the data available on the KITAB/OpenITI Corpus.  The KITAB Project is funded by ERC. All right reserved as per Apache Licence... 
		</div>
	</div>"""
    full_html += footer
    return full_html


def create_html_file(data):
    print("SAVING AS", book_name + ".html")
    with open(book_name + ".html", "w", encoding="utf-8") as e:
        e.write(html_open())

        e.write(data)
        e.write(html_close())


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


html_object = html_builder(data)
create_html_file(html_object)
