# -*- coding: utf-8 -*-
"""
Process chemical pages from wikipedia.
"""

import bz2
import re
from xml.sax.utils import unescape

title_matcher = re.compile("<title>(.*)</title>")
box_matcher = re.compile("{{(chembox|drugbox|infobox)")
def find_chembox(page,title):
    """
    Extract a chembox from the wiki page.
    """
    # Skip to start of <text> block
    text = page.find("<text")
    # Skip to start of chembox within <text>
    start = page.lower().find("{{chembox new",text)
    if start < 0:
        raise ValueError("Missing chembox in "+title)
    k = start+13

    # We are starting with a nesting level of 1.  Go until the end of the
    # page or until nesting level reaches zero.
    nesting = 1
    while True:
        if k >= len(page):
            # If we reach the end of the page, then we are missing }}
            raise ValueError("Mismatched {{Chembox new ... }} in "+title)
            return ""
        elif page[k:k+2] == "{{":
            # Increase nesting level on {{
            nesting += 1
            k += 2
        elif page[k:k+2] == "}}":
            # Decrease nesting level on }}
            # If nesting level reaches zero we are at the end of the box
            nesting -= 1
            k += 2
            if nesting == 0:
                chembook_end = k
                return page[start:k]
        elif page[k:].startswith("&lt;!--"):
            # Skip escaped XML comment
            k = page.find('--&gt;',k+4)
            if k < 0:
                raise ValueError("Mismatched <!--  ... --> in "+title)
        else:
            # Default is move to next character.
            k+=1

def next_page(file):
    """
    Get the next title/chembox
    """
    # Skip header
    while True:
        line = file.readline()
        if line.startswith("  <page>"):
            break
        if line == "":
            return None,""

    # Read page
    lines = [line]
    while True:
        line = file.readline()
        lines += [line]
        if line.startswith("  </page>"):
            break

    # Convert to a long string
    page = "".join(lines)
    match = title_matcher.search(page)
    title = match.group(1)
    chembox = find_chembox(page,title)
    chembox = unescape(chembox.decode('UTF-8'))
    return title,chembox

density_matcher = re.compile(r"\|\s*[Dd]ensity\s*=\s*([^|]*)\s*\|")
def find_density(chembox,title):
    match = density_matcher.search(chembox)
    if not match:
        return None,""

    # Convert spaces
    density = match.group(1)
    for form in ["&nbsp;","&thinsp;"]:
        density = density.replace(form," ")

    # Regularize units
    for form,becomes in [("&middot;"," "),
                         (u"·"," "),
                         ("&minus;","-"),
                         (u"−","-"),
                         (u"³","<sup>3</sup>"),
                         (u"°",""),
                         ("&deg;"," "),
                         ]:
        density = density.replace(form,becomes)

    for form in [
                 "kg/dm<sup>3</sup>",
                 "kg dm<sup>-3</sup>",
                 "kg.dm<sup>-3</sup>",
                 "kg/dm^3","kg/dm3",
                 "kg/L", "kg/l",
                 "kg l<sup>-1</sup>",
                 ]:
        density = density.replace(form,"#mL")#"g/cm**3")

    for form in [
                 "mg/cm<sup>3</sup>",
                 "mg cm<sup>-3</sup>",
                 "mg.cm<sup>-3</sup>",
                 "g/L","g/l",
                 "g L<sup>-1</sup>",
                 "g.L<sup>-1</sup>",
                 "g/dm<sup>3</sup>",
                 "g dm<sup>-3</sup>",
                 "g.dm<sup>-3</sup>",
                 "kg/m3",
                 "kg/m<sup>3</sup>",
                 "kg m<sup>-3</sup>",
                 "kg m-3",
                 "kg.m<sup>-3</sup>",
                 ]:
        density = density.replace(form,"#L")#"g/L")

    for form in [
                 "g/cm<sup>3</sup>",
                 "g cm<sup>-3</sup>",
                 "g.cm<sup>-3</sup>",
                 "g/cm^3","g/cm3","g/cc",
                 "g/mL", "g/ml",
                 "g ml<sup>-1</sup>",
                 ]:
        density = density.replace(form,"#mL")#"g/cm**3")
    density = density.strip()

    # If empty return None
    if density == "":
        return None,""
    #print density,"===",title#,match.group(1).strip()

    # Split into density/caveat
    endvalue = density.find(' ')
    if endvalue>0:
        value = density[:endvalue].strip()
        caveat = density[endvalue+1:].strip()
    else:
        value = density
        caveat = ""

    # Missing density?
    if value in ["-","?"]:
        return None,caveat

    # Floating point density?
    try:
        return float(value),caveat
    except:
        pass

    # European decimal point ','?
    try:
        return float(value.replace(',','.')),caveat
    except:
        pass

    # Value range?
    try:
        lo,hi = value.split('-')
        return (float(lo)+float(hi))/2,density
    except:
        pass

    # Unknown
    print(title,"unparsed density   -->   ",density)
    return None,density


def process_file(file):
    while True:
        try:
            title,chembox = next_page(file)
        except ValueError as msg:
            print(msg)
        else:
            if title == None:
                break
            density, caveat = find_density(chembox,title)
            #if density != None: print title,density,'::',caveat

def main():
    import sys
    iname = 'chempages.xml.bz2' if len(sys.argv) < 2 else sys.argv[2]
    ifile = bz2.BZ2File(iname) if iname.endswith('bz2') else open(iname,'rU')
    process_file(ifile)

if __name__ == "__main__":
    main()
