#! /usr/bin/env python

# This program is public domain.
"""
Find wikipedia chemical pages.

Usage:
   wget http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
   python extractchem.py

Extract all pages from enwiki-latest-pages-articles.xml.bz2
containing "{{chembox new", printing them to stdout.
For the 3.6 Gb compressed wiki database of March 2008, this
operation takes 100 minuits on a 2GHz pentium, yielding 3663
pages, 1653 of which have density information.
"""

import sys
import bz2

def next_page(fid):
    # Skip header
    while True:
        line = fid.readline()
        if line.startswith("  <page>"):
            break
        if line == "":
            return None, False

    # Read page
    page = [line]
    has_chembox = False
    while True:
        line = fid.readline()
        page.append(line)
        if line.startswith("  </page>"):
            break
        parts = line.split("{{")
        if len(parts) != 2:
            continue
        box = parts[1][:15].lower()
        if (box.startswith("chembox")
            or box.startswith("infobox mineral")
            or box.startswith("infobox drug")
            or box.startswith("drugbox")
            ):
            has_chembox = True
    # Skip talk pages, etc.
    if has_chembox:
        has_chembox = any("<ns>0</ns>" in line for line in page)

    return page,has_chembox

def process_file(ifile, ofile):
    count = 0
    chem_pages = 0
    while True:
        page, has_chembox = next_page(ifile)
        if page is None: break
        count += 1
        if has_chembox:
            chem_pages += 1
            print("%d of %d"%(chem_pages, count))
            print("".join(page), file=ofile, newline=False)

LATEST = 'enwiki-latest-pages-articles.xml.bz2'
OUTFILE = 'chempages.xml.bz2'
def main():
    iname = LATEST if len(sys.argv)<2 else sys.argv[1]
    oname = OUTFILE if len(sys.argv) < 3 else sys.argv[2]
    ifile = bz2.BZ2File(iname) if iname.endswith('bz2') else open(iname)
    ofile = bz2.BZ2File(oname,'w') if oname.endswith('bz2') else open(oname,'w')
    process_file(ifile,ofile)

if __name__ == "__main__":
    main()
