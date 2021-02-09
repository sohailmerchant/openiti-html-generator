"""Configuration file for replace operations"""

import re

def format_section_title(m):
    """Format the results of the find part of a re.sub operation
    to feed into the replace part.

    Args:
        m (match object)
    """
    pipes = m.group(1)
    title = m.group(2)
    #title_link = re.sub(r"\( *([^\(]*) *\)", r"\1", title).strip() # remove parenthesis from title
    #title_link = re.sub(r"""<span id='ms\d+'></span>""", "", title_link)
    #title_link = re.sub(" *<.+> *", " ", title_link) # remove all tags within title
    title_link = "temp"
    if "$" in pipes:
        return "<h{0} class='dic-item l{0}' id='{1}'>{2}</h{0}>\n".format(3, title_link, title)
    else:
        return "<h{0} class='l{0}' id='{1}'>{2}</h{0}>\n".format(len(pipes), title_link, title)

repl = [

    # remove superfluous characters:
    {
        "ptrn": r'~~',
        "repl": r""
    },

    {
        "ptrn": r"# Page",
        "repl": r"Page"
    },

    # remove header:
    
    {
        "ptrn": r"######OpenITI#.+?#META#Header#End#[\r\n]+(?:PageV0+P0+[\r\n]+)?",
        "repl":  r"\n",
        "flags": re.DOTALL
    }, 
    
    # tag milestones:
    
    {
        "ptrn": r'(ms\d+)',
        "repl":  r"<span id='\1'></span>",
        "flags": re.DOTALL
    }, 

    # tag poetry:
    
    {
        "ptrn": r"[\r\n]+# (.*)%~%(.*)",
        "repl":  r"""
            <p class='poetry'>
                <span class='hemistich-1'>\1</span>
                <span class='hemistich-2'>\2</span>
            </p>
            """
    }, 

    # tag paragraphs: 

    {
        "ptrn": r"[\r\n]+# (.+?)(?=[\r\n]+#|\Z|[\r\n]*<p)",
        "repl":  r"\n<p>\n\1\n</p>\n",
        "flags": re.DOTALL
    }, 

    # page numbers:

    {
        "ptrn": r'PageV([^P]+)P(\w+)',
        "repl":  r"""
            <div class='pageno-container'>
                <a class='pageno' href='#' id='v\1p\2'> Vol. \1, p. \2</a>
            </div>
            """,
    }, 

    # Editorial sections and paratext:
    
    {
        "ptrn": r"### \|([A-Z]+)\|\s+(.*?)(?=###)",
        "repl":  r"<div class='\1'>\n\2</div>\n",
        "flags": re.DOTALL
    }, 

    # section titles: 

    {
        "ptrn": "### ([\$\|]+) (.*)",
        "repl":  format_section_title,
    }, 

    # Qur'an quotes:

    {
        "ptrn": r'@QB@\s?(.*?)@QE@\s?',
        "repl":  r"<span class='quran'>\1</span>",
        "flags": re.DOTALL
    }, 


    # isnads:

    {
        "ptrn": r'@Auto_ISB@\s(W*.+)\s@Auto_ISE@', # is the W in this regex correct?
        "repl":  r"<span class='isnad'>\1</span>",
        "flags": re.DOTALL
    }, 


    ]
