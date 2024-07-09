"""
Extract all pages from enwiki-latest-pages-articles.xml.bz2
containing "{{chembox new", printing them to stdout.
For the 3.6 Gb compressed wiki database of March 2008, this
operation takes 100 minuits on a 2GHz pentium, yielding 3663
pages, 1653 of which have density information.
"""

import bz2

def next_page(file):
    # Skip header
    while True:
        line = file.readline()
        if line.startswith("  <page>"):
            break
        if line == "":
            return []

    # Read page
    page = line
    has_chembox = False
    while True:
        line = file.readline()
        if "{{chembox new" in line.lower():
            has_chembox = True
        page += line
        if line.startswith("  </page>"):
            break
    return page,has_chembox

def process_file(file):
    while True:
        page, has_chembox = next_page(file)
        if page == []:
            break
        if has_chembox:
            print("".join(page), newline=False)

if __name__ == "__main__":
    fid = bz2.BZ2File('enwiki-latest-pages-articles.xml.bz2')
    process_file(fid)
