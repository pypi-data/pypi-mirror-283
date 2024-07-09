#!/usr/bin/python -u
# -*- encoding: utf-8 -*-

import os, tempfile
import base64
import cgi
import io
import re
from urllib.parse import quote

import numpy as np

import scipy.interpolate as interpolate
import scipy.optimize as optimize

os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import cgitb; cgitb.enable()


form = cgi.FieldStorage()
#form = cgi.FieldStorage()
#title = form['title'].value

# Get data from fields
if form.getvalue('title'):
    title = form.getvalue('title')
else:
    title = "Not entered"

if form.getvalue('subject'):
    subject = form.getvalue('subject')
else:
    subject = "Not set"

if form.getvalue('seq'):
    sequence = form['seq'].value
else:
    sequence = "Not entered"

#if (form.has_key("title") and form.has_key("seq")):
#    print "<H1>Error</H1>"
#    print "Please fill in the name and addr fields."
#    return

#if not (form.has_key("title") and form.has_key("seq")):
#    print "<H1>Error</H1>"
#    print "Please fill in the title and sequence fields."
#    return

contrast = form['sol'].value
deuteration = form['protd'].value
exchange = form['prote'].value
conc = form['conc'].value

sequence = ''.join(i for i in sequence if not i.isdigit())
sequence = sequence.replace(' ', '')

# Content-Type: text/html\r\n
#<?php header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0'); ?>
#<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
print("""\
Content-Type: text/html\n
<?php header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0'); ?>
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
<meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">
<head><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title>Biomolecular Scattering Length Density Calculator</title>
</head>

<body bgcolor="FFFFFF">
<center>
<font size="+3">B</font><font size="+2">iomolecular</font>
<font size="+3">S</font><font size="+2">cattering</font>
<font size="+3">L</font><font size="+2">ength</font>
<font size="+3">D</font><font size="+2">ensity</font>
<font size="+3">C</font><font size="+2">alculator</font>
</center>

<br><hr><br>
""")

def strip_comments(s):
    """
    Allow comments in triple-quoted strings that are stripped before printing.
    """
    # Strip full lines. Use positive lookbehind so that we can see if there
    # is a newline in front without consuming the newline. Without this we
    # cannot have consecutive commented out lines.
    s = re.sub(r"(?<=\n)#.*\n", "", s)
    # Strip trailing comments
    s = re.sub(r"#.*", "")
    return s

print(strip_comments(f"""\
<center>
<html><body>

<p><b> Table 1. The Total number of residues, Chemical composition, Molecular weight in kilodaltons, scattering length, scattering length density (&#x3c1;), molecular volume and number of exchangeable hydrogens for the inputed protein given it's sequence, % deuteration, % D<sub>2</sub>O concentration and % exchange.</b>

</body></html>
# % subject
#<p><b> The value given below have been taken
<center>

<html><body>
<p>The sequence submitted was called "{title}"</p>
</body></html>
<justify>
<html><body>
<p>The sequence submitted was "{sequence}"</p>
</body></html>
</justify>
<html><body>
<p>The percentage of D<sub>2</sub>O in the solution is "{contrast}"</p>
</body></html>
<html><body>
<p>The percentage of deuteration is "{deuteration}"</p>
</body></html>
<html><body>
<p>The percentage of exchange is "{exchange}"</p>
</body></html>
<center/>

<html><body>
<p>The concentration of the biomolecule in mg/ml is "{conc}"</p>
</body></html>

<center/>

"""))

contrast = float(contrast)
contrast1 = float(contrast)
deuteration = float(deuteration)
exchange = float(exchange)
conc = float(conc)

#Defines variables
mw_H2O = 0
mw_D2O = 0
mw_dD2O = 0
mw_dH2O = 0
sl_H2O = 0
sl_D2O = 0
sl_dD2O = 0
sl_dH2O = 0
mol_vol = 0
amino = 0
hydro = float (0.0)
ex = float (0.0)
C = 0
N = 0
O = 0
H = 0
S = 0
P = 0

if subject == 'RNA':
    #Reads sequence and calculates RNA variables
    for residue in sequence :
        if residue == "A" or residue == "a" :
            mol_vol = mol_vol + 314.0
            mw_H2O = mw_H2O + 328.23
            mw_D2O = mw_D2O + 331.23 
            mw_dH2O = mw_dH2O + 336.23 
            mw_dD2O = mw_dD2O + 339.23
            sl_H2O = sl_H2O + 112.3
            sl_D2O = sl_D2O + 143.5
            sl_dH2O = sl_dH2O + 195.4
            sl_dD2O = sl_dD2O + 226.8
            amino = amino + 1
            hydro = hydro + 11
            ex = ex + 3
            C = C + 10
            N = N + 5
            O = O + 6
            H = H + 11
            P = P + 1

        if residue == "G" or residue == "g" :
            mol_vol = mol_vol + 326.3
            mw_H2O = mw_H2O + 344.23
            mw_D2O = mw_D2O + 348.23
            mw_dH2O = mw_dH2O + 351.23
            mw_dD2O = mw_dD2O + 355.23
            sl_H2O = sl_H2O + 118.1
            sl_D2O = sl_D2O + 159.8
            sl_dH2O = sl_dH2O + 190.8
            sl_dD2O = sl_dD2O + 232.6
            amino = amino + 1
            hydro = hydro + 11
            ex = ex + 4
            C = C + 10
            N = N + 5
            O = O + 7
            H = H + 11
            P = P + 1

        if residue == "C" or residue == "c" :
            mol_vol = mol_vol + 285.6
            mw_H2O = mw_H2O + 304.2
            mw_D2O = mw_D2O + 307.2
            mw_dH2O = mw_dH2O + 312.2
            mw_dD2O = mw_dD2O + 315.2
            sl_H2O = sl_H2O + 92.7
            sl_D2O = sl_D2O + 123.9
            sl_dH2O = sl_dH2O + 175.8
            sl_dD2O = sl_dD2O + 207.2
            amino = amino + 1
            hydro = hydro + 11
            ex = ex + 3
            C = C + 9
            N = N + 3
            O = O + 7
            H = H + 11
            P = P + 1

        if residue == "U" or residue == "u" :
            mol_vol = mol_vol + 282.3
            mw_H2O = mw_H2O + 305.18
            mw_D2O = mw_D2O + 307.18
            mw_dH2O = mw_dH2O + 313.18
            mw_dD2O = mw_dD2O + 315.18
            sl_H2O = sl_H2O + 92.8
            sl_D2O = sl_D2O + 113.6
            sl_dH2O = sl_dH2O + 175.9
            sl_dD2O = sl_dD2O + 196.9
            amino = amino + 1
            hydro = hydro + 10
            ex = ex + 2
            C = C + 9
            N = N + 2
            O = O + 8
            H = H + 10
            P = P + 1

elif subject == 'DNA':
    #Reads sequence and calculates DNA variables
    for residue in sequence :
        if residue == "A" or residue == "a" :
            mol_vol = mol_vol + 314.0
            mw_H2O = mw_H2O + 312.23
            mw_D2O = mw_D2O + 314.23
            mw_dH2O = mw_dH2O +  321.23
            mw_dD2O = mw_dD2O + 323.23
            sl_H2O = sl_H2O + 106.6
            sl_D2O = sl_D2O + 127.4
            sl_dH2O = sl_dH2O + 200.0
            sl_dD2O = sl_dD2O + 221.1
            amino = amino + 1
            hydro = hydro + 11
            ex = ex + 2
            C = C + 10
            N = N + 5
            O = O + 5
            H = H + 11
            P = P + 1

        if residue == "G" or residue == "g" :
            mol_vol = mol_vol + 326.3
            mw_H2O = mw_H2O + 328.23
            mw_D2O = mw_D2O + 331.23
            mw_dH2O = mw_dH2O + 336.23
            mw_dD2O = mw_dD2O + 339.23
            sl_H2O = sl_H2O + 112.4
            sl_D2O = sl_D2O + 143.6
            sl_dH2O = sl_dH2O + 195.4
            sl_dD2O = sl_dD2O + 226.9
            amino = amino + 1
            hydro = hydro + 11
            ex = ex + 3
            C = C + 10
            N = N + 5
            O = O + 6
            H = H + 11
            P = P + 1

        if residue == "C" or residue == "c" :
            mol_vol = mol_vol + 285.6
            mw_H2O = mw_H2O + 288.2
            mw_D2O = mw_D2O + 290.2
            mw_dH2O = mw_dH2O + 297.2
            mw_dD2O = mw_dD2O + 299.2
            sl_H2O = sl_H2O + 86.9
            sl_D2O = sl_D2O + 107.7
            sl_dH2O = sl_dH2O + 180.4
            sl_dD2O = sl_dD2O + 201.4
            amino = amino + 1
            hydro = hydro + 11
            ex = ex + 2
            C = C + 9
            N = N + 3
            O = O + 6
            H = H + 11
            P = P + 1

        if residue == "T" or residue == "t" :
            mol_vol = mol_vol + 308.7
            mw_H2O = mw_H2O + 303.21
            mw_D2O = mw_D2O + 304.21
            mw_dH2O = mw_dH2O + 314.21
            mw_dD2O = mw_dD2O + 315.21
            sl_H2O = sl_H2O + 86.2
            sl_D2O = sl_D2O + 96.6
            sl_dH2O = sl_dH2O + 200.5
            sl_dD2O = sl_dD2O + 211.2
            amino = amino + 1
            hydro = hydro + 10
            ex = ex + 1
            C = C + 10
            N = N + 2
            O = O + 7
            H = H + 12
            P = P + 1

elif subject == 'Protein':
    #Reads protein sequence and calculates base variables
    for residue in sequence :
        if residue == "G" or residue == "g" :
            #Glycine
            mol_vol = mol_vol + 59.9
            mw_H2O = mw_H2O + 57.07
            mw_D2O = mw_D2O + 58.07
            mw_dH2O = mw_dH2O + 59.07
            mw_dD2O = mw_dD2O + 60.07
            sl_H2O = sl_H2O + 17.28
            sl_D2O = sl_D2O + 27.69
            sl_dH2O = sl_dH2O + 38.055
            sl_dD2O = sl_dD2O + 48.5
            amino = amino + 1
            hydro = hydro + 3
            ex = ex + 1
            C = C + 2
            N = N +1
            O = O
            H = H + 3
        elif residue == "A" or residue == "a" :
            #Alanine
            mol_vol = mol_vol + 87.8
            mw_H2O = mw_H2O + 71.09
            mw_D2O = mw_D2O + 72.09
            mw_dH2O = mw_dH2O + 75.07
            mw_dD2O = mw_dD2O + 76.07
            sl_H2O = sl_H2O + 16.45
            sl_D2O = sl_D2O + 26.86
            sl_dH2O = sl_dH2O + 58.043
            sl_dD2O = sl_dD2O + 68.52
            amino = amino + 1
            hydro = hydro + 5
            ex = ex + 1
            C = C + 3
            N = N + 1
            O = O + 1
            H = H + 5
        elif residue == "C" or residue == "c" :
            #Cysteine
            mol_vol = mol_vol + 105.4
            mw_H2O = mw_H2O + 103.16
            mw_D2O = mw_D2O + 104.16
            mw_dH2O = mw_dH2O + 106
            mw_dD2O = mw_dD2O + 108
            sl_H2O = sl_H2O + 19.30
            sl_D2O = sl_D2O + 40.13
            sl_dH2O = sl_dH2O + 54.219
            sl_dD2O = sl_dD2O + 71.37
            amino = amino + 1
            hydro = hydro + 5
            ex = ex + 2
            C = C + 3
            N = N + 1
            O = O + 1
            S = S + 1
            H = H + 5
        elif residue == "D" or residue == "d" :
            #Aspartic acid
            mol_vol = mol_vol + 115.4
            mw_H2O = mw_H2O + 115.1
            mw_D2O = mw_D2O + 117.1
            mw_dH2O = mw_dH2O + 118
            mw_dD2O = mw_dD2O + 122
            sl_H2O = sl_H2O + 38.45
            sl_D2O = sl_D2O + 48.86
            sl_dH2O = sl_dH2O + 65.877
            sl_dD2O = sl_dD2O + 80.10
            amino = amino + 1
            hydro = hydro + 4
            ex = ex + 1
            C = C + 4
            N = N + 1
            O = O + 3
            H = H + 4
        elif residue == "E" or residue == "e" :
            #Glutamic acid
            mol_vol = mol_vol + 140.9
            mw_H2O = mw_H2O + 129.13
            mw_D2O = mw_D2O + 131.13
            mw_dH2O = mw_dH2O + 134
            mw_dD2O = mw_dD2O + 136
            sl_H2O = sl_H2O + 37.62
            sl_D2O = sl_D2O + 48.03
            sl_dH2O = sl_dH2O + 85.874
            sl_dD2O = sl_dD2O + 101
            amino = amino + 1
            hydro = hydro + 6
            ex = ex + 1
            C = C + 5
            N = N + 1
            O = O + 3
            H = H + 4
        elif residue == "F" or residue == "f" :
            #Phenylalanine
            mol_vol = mol_vol + 189.7
            mw_H2O = mw_H2O + 147.19
            mw_D2O = mw_D2O + 148.19
            mw_dH2O = mw_dH2O + 155
            mw_dD2O = mw_dD2O + 156
            sl_H2O = sl_H2O + 41.39
            sl_D2O = sl_D2O + 51.8
            sl_dH2O = sl_dH2O + 124.606
            sl_dD2O = sl_dD2O + 135.1
            amino = amino + 1
            hydro = hydro + 9
            ex = ex + 1
            C = C + 9
            N = N + 1
            O = O + 1
            H = H + 9
        elif residue == "H" or residue == "h":
            #Histidine
            mol_vol = mol_vol + 156.3
            mw_H2O = mw_H2O + 137.15
            mw_D2O = mw_D2O + 139.15
            mw_dH2O = mw_dH2O + 142
            mw_dD2O = mw_dD2O + 144
            sl_H2O = sl_H2O + 49.59
            sl_D2O = sl_D2O + 65.21
            sl_dH2O = sl_dH2O + 99.638
            sl_dD2O = sl_dD2O + 117.3
            amino = amino + 1
            hydro = hydro + 7
            ex = ex + 1.5
            C = C + 6
            N = N + 3
            O = O + 1
            H = H + 6.5
        elif residue == "I" or residue == "i" :
            #Isoleucine
            mol_vol = mol_vol + 166.1
            mw_H2O = mw_H2O + 113
            mw_D2O = mw_D2O + 115
            mw_dH2O = mw_dH2O + 123
            mw_dD2O = mw_dD2O + 124
            sl_H2O = sl_H2O + 13.96
            sl_D2O = sl_D2O + 24.37
            sl_dH2O = sl_dH2O + 118.01
            sl_dD2O = sl_dD2O + 128.5
            amino = amino + 1
            hydro = hydro + 11
            ex = ex + 1
            C = C +6
            N = N + 1
            O = O + 1
            H = H + 11
        elif residue == "K" or residue == "k":
            #Lysine
            mol_vol = mol_vol + 172.7
            mw_H2O = mw_H2O + 128
            mw_D2O = mw_D2O + 131
            mw_dH2O = mw_dH2O + 137
            mw_dD2O = mw_dD2O + 140
            sl_H2O = sl_H2O + 15.86
            sl_D2O = sl_D2O + 57.52
            sl_dH2O = sl_dH2O + 113.219
            sl_dD2O = sl_dD2O + 151.2
            amino = amino + 1
            hydro = hydro + 13
            ex = ex + 4
            C = C + 6
            N = N + 2
            O = O + 1
            H = H + 13
        elif residue == "L" or residue == "l":
            #Leucine
            mol_vol = mol_vol + 168.0
            mw_H2O = mw_H2O + 113.17
            mw_D2O = mw_D2O + 114.17
            mw_dH2O = mw_dH2O + 123
            mw_dD2O = mw_dD2O + 124
            sl_H2O = sl_H2O + 13.96
            sl_D2O = sl_D2O + 24.37
            sl_dH2O = sl_dH2O + 118.01
            sl_dD2O = sl_dD2O + 128.5
            amino = amino + 1
            hydro = hydro + 11
            ex = ex + 1
            C = C + 6
            N = N + 1
            O = O + 1
            H = H + 11
        elif residue == "M" or residue == "m":
            #Methionine
            mol_vol = mol_vol + 165.2
            mw_H2O = mw_H2O + 131.21
            mw_D2O = mw_D2O + 132.21
            mw_dH2O = mw_dH2O + 139
            mw_dD2O = mw_dD2O + 140
            sl_H2O = sl_H2O + 17.64
            sl_D2O = sl_D2O + 28.05
            sl_dH2O = sl_dH2O + 100.869
            sl_dD2O = sl_dD2O + 111.4
            amino = amino + 1
            hydro = hydro + 9
            ex = ex + 1
            C = C + 5
            N = N + 1
            O = O + 1
            S = S + 1
            H = H + 9
        elif residue == "N" or residue == "n":
            #Asparagine
            mol_vol = mol_vol + 115.4
            mw_H2O = mw_H2O + 130.12
            mw_D2O = mw_D2O + 133.12
            mw_dH2O = mw_dH2O + 133
            mw_dD2O = mw_dD2O + 136
            sl_H2O = sl_H2O + 34.56
            sl_D2O = sl_D2O + 65.08
            sl_dH2O = sl_dH2O + 65.08
            sl_dD2O = sl_dD2O + 97.04
            amino = amino + 1
            hydro = hydro + 6
            ex = ex + 3
            C = C + 4
            N = N + 2
            O = O + 2
            H = H + 6
        elif residue == "P" or residue == "p":
            #Proline
            mol_vol = mol_vol + 123.3
            mw_H2O = mw_H2O + 97.13
            mw_D2O = mw_D2O + 97.13
            mw_dH2O = mw_dH2O + 104
            mw_dD2O = mw_dD2O + 104
            sl_H2O = sl_H2O + 22.27
            sl_D2O = sl_D2O + 22.27
            sl_dH2O = sl_dH2O + 95.16
            sl_dD2O = sl_dD2O + 95.16
            amino = amino + 1
            hydro = hydro + 7
            ex = ex
            C = C + 5
            N = N + 1
            O = O + 1
            H = H + 7
        elif residue == "Q" or residue == "q":
            #Glutamine
            mol_vol = mol_vol + 145.1
            mw_H2O = mw_H2O + 128.14
            mw_D2O = mw_D2O + 129.14
            mw_dH2O = mw_dH2O + 133
            mw_dD2O = mw_dD2O + 136
            sl_H2O = sl_H2O + 33.73
            sl_D2O = sl_D2O + 64.97
            sl_dH2O = sl_dH2O + 85.692
            sl_dD2O = sl_dD2O + 117
            amino = amino + 1
            hydro = hydro + 8
            ex = ex + 3
            C = C + 5
            N = N + 2
            O = O + 2
            H = H + 8
        elif residue == "R" or residue == "r":
            #Arginine
            mol_vol = mol_vol + 188.2
            mw_H2O = mw_H2O + 154.2
            mw_D2O = mw_D2O + 159.2
            mw_dH2O = mw_dH2O + 161
            mw_dD2O = mw_dD2O + 166
            sl_H2O = sl_H2O + 34.66
            sl_D2O = sl_D2O + 97.14
            sl_dD2O = sl_dD2O + 170
            amino = amino + 1
            hydro = hydro + 13
            ex = ex + 6
            C = C + 6
            N = N + 4
            O = O + 1
            H = H + 13
        elif residue == "S" or residue == "s":
            #Serine
            mol_vol = mol_vol + 91.7
            mw_H2O = mw_H2O + 87.09
            mw_D2O = mw_D2O + 89.09
            mw_dH2O = mw_dH2O + 90
            mw_dD2O = mw_dD2O + 92
            sl_H2O = sl_H2O + 22.25
            sl_D2O = sl_D2O + 43.08
            sl_dH2O = sl_dH2O + 47.634
            sl_dD2O = sl_dD2O + 74.32
            amino = amino + 1
            hydro = hydro + 5
            ex = ex + 2
            C = C + 3
            N = N + 1
            O = O + 2
            H = H + 5
        elif residue == "T" or residue == "t":
            #Threonine
            mol_vol = mol_vol + 118.3
            mw_H2O = mw_H2O + 91.12
            mw_D2O = mw_D2O + 93.12
            mw_dH2O = mw_dH2O + 96
            mw_dD2O = mw_dD2O + 100
            sl_H2O = sl_H2O + 21.42
            sl_D2O = sl_D2O + 42.24
            sl_dH2O = sl_dH2O + 73.425
            sl_dD2O = sl_dD2O + 94.31
            amino = amino + 1
            hydro = hydro + 7
            ex = ex + 2
            C = C + 4
            N = N + 1
            O = O + 2
            H = H + 7
        elif residue == "V" or residue == "v":
            #Valine
            mol_vol = mol_vol + 138.8
            mw_H2O = mw_H2O + 99.15
            mw_D2O = mw_D2O + 100.15
            mw_dH2O = mw_dH2O + 107
            mw_dD2O = mw_dD2O + 108
            sl_H2O = sl_H2O + 14.79
            sl_D2O = sl_D2O + 25.20
            sl_dH2O = sl_dH2O + 98.292
            sl_dD2O = sl_dD2O + 108.54
            amino = amino + 1
            hydro = hydro + 9
            ex = ex + 1
            C = C + 5
            N = N + 1
            O = O + 1
            H = H + 9
        elif residue == "W" or residue == "w":
            #Tryptophan
            mol_vol = mol_vol + 227.9
            mw_H2O = mw_H2O + 186.23
            mw_D2O = mw_D2O + 187.23
            mw_dH2O = mw_dH2O + 195
            mw_dD2O = mw_dD2O + 196
            sl_H2O = sl_H2O + 60.35
            sl_D2O = sl_D2O + 81.18
            sl_dH2O = sl_dH2O + 153.931
            sl_dD2O = sl_dD2O + 164.5
            amino = amino + 1
            hydro = hydro + 10
            ex = ex + 2
            C = C + 11
            N = N + 2
            O = O + 1
            H = H + 10
        elif residue == "Y" or residue == "y":
            #Tyrosine
            mol_vol = mol_vol + 191.2
            mw_H2O = mw_H2O + 163.19
            mw_D2O = mw_D2O + 165.19
            mw_dH2O = mw_dH2O + 170
            mw_dD2O = mw_dD2O + 172
            sl_H2O = sl_H2O + 47.19
            sl_D2O = sl_D2O + 68.02
            sl_dH2O = sl_dH2O + 134.786
            sl_dD2O = sl_dD2O + 140.9
            amino = amino + 1
            hydro = hydro + 9
            ex = ex + 2
            C = C + 9
            N = N + 1
            O = O + 2
            H = H + 9


###Adds water to mw values
mw_H2O = (mw_H2O + 18)/1000
mw_D2O = (mw_D2O + 20)/1000
mw_dH2O = (mw_dH2O + 18)/1000
mw_dD2O = (mw_dD2O + 20)/1000
H = H + 2
O = O + 1

#Adds water to and outputs molecular volume
mol_vol = mol_vol + 30

##Total number of hydrogens
hydro = hydro + 2

### Exchangable hydrogens
ex = ex + 2

# Calculating the molecular weight, SL and SLD
#exdec = exchange /100
#mw_H2O = mw_H2O / 1000
contrast = contrast /100
exchange = exchange /100
deuteration = deuteration /100
#e = 0
#e = contrast * exchange * (ex / hydro)
#print " %s." %(deuteration)
#print " %s." %(exchange)
#print " %s." %(contrast)
#print " %s." %(e)
###e = 0
##
##e = (ex / hydro)
##
###f = (contrast * exchange * e)*100
##
##print " %s." %(e)

mw_hp_contrast = ((mw_D2O * (contrast * exchange))+(mw_H2O * (1-(contrast * exchange))))
mw_dp_contrast = ((mw_dD2O * (contrast * exchange))+(mw_dH2O * (1-(contrast * exchange))))
mw_contrast = ((mw_dp_contrast * (deuteration))+(mw_hp_contrast * (1-(deuteration))))

#mw_contrast = mw_contrast/1000

sl_hp_contrast = ((sl_D2O * (contrast * exchange))+(sl_H2O * (1-(contrast * exchange))))
sl_dp_contrast = ((sl_dD2O * (contrast * exchange))+(sl_dH2O * (1-(contrast * exchange))))
sl_contrast = ((sl_dp_contrast * (deuteration))+(sl_hp_contrast * (1-(deuteration))))
sl_contrast1 = (sl_contrast/ 10)
sl_contrast = (sl_contrast * 10)
sld = (sl_contrast/mol_vol)
density = (1e27 * mw_contrast)/(mol_vol*6.0221413e23)
volume_frac = conc / (density * 1e3)
sldw = ((contrast*100) * 0.0693)-0.554
sldc = sld - sldw
sldcc = (sldc*sldc)
vol = mol_vol*1e-24
intensity = volume_frac * vol * (sldcc * 1e20)

# Display outputs
#print """\
#Content-Type: text/html\n
#"""
print(strip_comments(f"""\
<p> </p>
Total number of residues is {amino}.
<p> </p>
Chemical composition C{C} N{N} O{O} S{S} H{H} P{P}
<p> </p>
The molecular weight of the biomolecule is {round(mw_contrast,3)} kDa
<p> </p>
The Scattering length is {round(sl_contrast1,2)} x10<sup>-4</sup>&#x212b;
<p> </p>
The scattering length density (&#x3c1;<sub>m</sub>) of the molecule is {round(sld, 3)}x10<sup>-6</sup>&#x212b;<sup>-2</sup>
<p> </p>
The scattering length denisty (&#x3c1;<sub>s</sub>) of the solvent is {round(sldw,3)}x10<sup>-6</sup>&#x212b;<sup>-2</sup>
<p> </p>
The molecular volume is {round(mol_vol, 1)}&#x212b;<sup>3</sup>
<p> </p>
The number of exchangable hydrogens at pH 7.0 is {ex}
<p> </p>
The density of the biomolecule is {round(density,2)} g/ml
<p> </p>
## Note: need double braces to suppress substitution for commented lines
#The volume fraction of the biomolecule is {{round(volume_frac,5)}}
#<p> </p>
#The vol of the biomolecule is {{vol}}
#<p> </p>
The estimate of intensity at zero angle I(0) of the biomolecule is {intensity:%.2g} cm<sup>-1</sup>
<p> </p>
<br>
<br>
<justify><b> Figure 1. The scattering length density (&#x3c1;) of the inputed protein (it's sequence, % deuteration <br> and % exchange) as a function of increasing D<sub>2</sub>O concentration (from 0 to 100% in 5% intervals).</b></justify>
#The total number of hydrogens is {{hydro}}
#<p> </p>
# {{e}}.
#<p> </p>
"""))

#makes the graph
sld = float(0.0)
mw = float(0.0)
d2o = 0
ier=0
xy = []
x = []
y = []
element = []
contrast = float(0.0)
#print "Contrast %s" % (contrast)
#print " %s." %(deuteration)
#print " %s." %(exchange)
#print " %s." %(contrast)
counter = 0

while contrast <= 1.05:
    mw_hp_contrast = ((mw_D2O * (contrast * exchange))+(mw_H2O * (1-(contrast * exchange))))
    mw_dp_contrast = ((mw_dD2O * (contrast * exchange))+(mw_dH2O * (1-(contrast * exchange))))
    mw_contrast = ((mw_dp_contrast * (deuteration))+(mw_hp_contrast * (1-(deuteration))))
    sl_hp_contrast = ((sl_D2O * (contrast * exchange))+(sl_H2O * (1-(contrast * exchange))))
    sl_dp_contrast = ((sl_dD2O * (contrast * exchange))+(sl_dH2O * (1-(contrast * exchange))))
    sl_contrast = ((sl_dp_contrast * (deuteration))+(sl_hp_contrast * (1-(deuteration))))
    sl_contrast =(sl_contrast * 10)
    sld =(sl_contrast/mol_vol)
    xy.append((contrast, sld))
    d2o = int(contrast*100)
    x.append(d2o)
    y.append(sld)
    contrast = contrast + 0.05

# plots the file
fig = plt.figure(1)
ov = 0
plt.plot(x, y, '-r.')
x = np.array(x)
y = np.array(y)
x2=np.array([0,10,20,30,40,50,60,70,80,90,100])
y2=np.array([-0.554, 0.139, 0.831, 1.52, 2.22, 2.91, 3.60, 4.29, 4.99, 5.68, 6.37])
plt.plot(x2, y2, '-b.')

over = y[ np.where( y > 6.37)]
p = np.count_nonzero(over)
if p > 0:
   ov = over[0]
else:
   ov = 0

if ov > 0:
   #print "<center>There is / are %s" % (p), " scattering length/s over 100% D2O</center>"
    print("""\
    <br><center>
    <p style="color: red; font-weight: bold;"> There is no match point for your system</p></center>
    """)

    #print '<p><p style="color: red"> <br><center> There is no match point for your system, please alter values !!! </center></p>'
    plt.legend([title, "Water"], bbox_to_anchor=(0.8, 0.3), loc=2, prop={'size':10}, borderaxespad=0.)
    plt.xlabel('% D$_{2}$O')
    plt.ylabel('SLD *10$^{-6}\AA^{-2}$')
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data

    uri = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.buf))
    print('<img src = "%s"/>' % uri)

else:
#   print ("Values exceed 100% D2O")
#else:
   x2=np.array([0,10,20,30,40,50,60,70,80,90,100])
   y2=np.array([-0.554, 0.139, 0.831, 1.52, 2.22, 2.91, 3.60, 4.29, 4.99, 5.68, 6.37])
   plt.plot(x2, y2, '-b.')
   p1=interpolate.PiecewisePolynomial(x, y[:,np.newaxis])
   p2=interpolate.PiecewisePolynomial(x2,y2[:,np.newaxis])
   def pdiff(x):
       return p1(x)-p2(x)
   xs=np.r_[x,x2]
   xs.sort()
   x_min=xs.min()
   x_max=xs.max()
   x_mid=xs[:-1]+np.diff(xs)/2
   roots=set()
   for val in x_mid:
       root,infodict,ier,mesg = optimize.fsolve(pdiff,val,full_output=True)
       # ier==1 indicates a root has been found
       if ier==1 and x_min<root<x_max:
           roots.add(root[0])
       #else:
        #  print ("No match point found")

   roots=list(roots)
   #print(np.column_stack(("%.2f" % roots[0],"%.2f" % p1(roots[0]))))
   #l = plt.axhline(linewidth=4, color='r')
   #l = plt.axhline(y=p1(roots[1]), xmin=0, xmax=0.1
   #print roots[0]
   #print sl_contrast
   #print ier
   #if ier == 1:
   l = plt.axhline(y=p1(roots[0]), xmin=0, xmax=(roots[0]/100))
   l = plt.axvline(x=roots[0], ymin=0, ymax=((p1(roots[0])/8)+0.125))
   l = plt.axhline(y=p1(roots[0]), xmin=0, xmax=(roots[0]/120))
   l = plt.axvline(x=roots[0], ymin=0, ymax=((p1(roots[0])/8)+0.125))
   plt.text(10, ((p1(roots[0]))+0.5), ( "Match point"), fontsize=15)
   plt.text(10, ((p1(roots[0]))+0.125), ( "%.2f" % roots[0], "%.2f" % p1(roots[0])), fontsize=15) 
   # "Molecule"
   plt.legend([title, "Water"], bbox_to_anchor=(0.80, 0.30), loc=2, prop={'size':10}, borderaxespad=0.)
   plt.xlabel('% D$_{2}$O')
   plt.ylabel('SLD *10$^{-6}\AA^{-2}$')

   #figtext(.02, .02, "Figure 1 : A graph of the scattering length density of a molecule as defined by its sequence, percentage deuteration and percentage exchange, as a function of increasing D2O concentration in a H2O : D2O solvent.")

   #import sys
   #if sys.platform == "win32":
     #  import os, msvcrt
    #   msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

   imgdata = io.BytesIO()
   fig.savefig(imgdata, format='png')
   imgdata.seek(0)  # rewind the data

   #print "Content-type: image/png\n"
   uri = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.buf))
   print('<img src = "%s"/>' % uri)

   #print "Content-Type: image/png\n"
   #plt.savefig(sys.stdout, format='png')
   #data_uri = open(sys.stdout, 'rb').read().encode('base64').replace('\n', '')
   #img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
   #print(img_tag)


#height="400" width="400"
#plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
#plt.show()
##
##    #else:
##     #   print ("No match point")
##    # writes a text file of the data
##    text_file = open("protein sld.txt", "w")
##    text_file.write("%D2O , SLD")
##    text_file.write("\n")
##    while counter != 21:
##        contr = int((xy[counter][0])*100)
##        contr = str((xy[counter][0])*100)
##        csld = str(xy[counter][1])
##        text_file.write(contr)
##        text_file.write(" , ")
##        text_file.write(csld)
##        text_file.write("\n")
##        counter = counter + 1
##    text_file.close()

print("""\
<br>
<br>
""")

print("<justify><b> Figure 2. The scattering length density (&#x3c1;) of the inputed protein (it's sequence, % D<sub>2</sub>O and <br>  % exchange) as a function of increasing percentage deuteration (from 0 to 100% in 5% intervals).<b></justify>")

print("<br>")


# deuteration graph
contrast1 = contrast1 /100
sld = float(0.0)
mw = float(0.0)
xy = []
x = []
y = []
element = []
deuteration = float(0.0)
deut = float(0.0)
#print " %s." %(deuteration)
#print " %s." %(exchange)
#print " %s." %(contrast1)
counter = 0
while deuteration <= 1.05:
    mw_hp_contrast = ((mw_D2O * (contrast1 * exchange))+(mw_H2O * (1-(contrast1 * exchange))))
    mw_dp_contrast = ((mw_dD2O * (contrast1 * exchange))+(mw_dH2O * (1-(contrast1 * exchange))))
    mw_contrast = ((mw_dp_contrast * (deuteration))+(mw_hp_contrast * (1-(deuteration))))
    sl_hp_contrast = ((sl_D2O * (contrast1 * exchange))+(sl_H2O * (1-(contrast1 * exchange))))
    sl_dp_contrast = ((sl_dD2O * (contrast1 * exchange))+(sl_dH2O * (1-(contrast1 * exchange))))
    sl_contrast = ((sl_dp_contrast * (deuteration))+(sl_hp_contrast * (1-(deuteration))))
    sl_contrast = (sl_contrast * 10)
    sld = (sl_contrast/mol_vol)
    xy.append((deuteration, sld))
    deut = (deuteration*100)
    x.append(deut)
    y.append(sld)
    deuteration = deuteration + 0.05

#Plots the file
fig1 = plt.figure(2)
ove = 0
plt.plot(x, y, '-m.')
x = np.array(x)
y = np.array(y)
x2=np.array([0,10,20,30,40,50,60,70,80,90,100])
y2=np.array([-0.554, 0.139, 0.831, 1.52, 2.22, 2.91, 3.60, 4.29, 4.99, 5.68, 6.37])
plt.plot(x2, y2, '-b.')
plt.xlim(0, 100)
#x2=np.array([0,10,20,30,40,50,60,70,80,90,100])
#   y2=np.array([-0.554, 0.139, 0.831, 1.52, 2.22, 2.91, 3.60, 4.29, 4.99, 5.68, 6.37])
#   plt.plot(x2, y2, '-b.')

overa = y[ np.where( y > 6.37)]
p1 = np.count_nonzero(overa)

if p1 > 0:
   ove = overa[0]
else:
   ove = 0

#print "P %s" %overa
#ov = over[1]

if ove > 0:
    #print "<br><center>There is /are %s" % (p1), " scattering length/s over 100% deuteration</center>"
    #print "<br><center> There is no match point for your system, please alter values !!! </center>"
    print("""\
    <br><center>
    <p style="color: red; font-weight: bold;"> There is no match point for your system </p></center>
    """)
    plt.legend([title, "Water"], bbox_to_anchor=(0.8, 0.30), loc=2, prop={'size':10}, borderaxespad=0.)
    plt.xlabel('% Deuteration')
    plt.ylabel('SLD *10$^{-6}\AA^{-2}$')

    imgdata = io.BytesIO()
    fig1.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data

    #print "Content-type: image/png\n"
    uri = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.buf))
    #print """/
    #<img height= height="600">
    #"""
    print('<img src = "%s"/ height="600" width="800">' % uri)

else:
#plt.axis(0, 100, 0, 4.0)
   p1=interpolate.PiecewisePolynomial(x, y[:,np.newaxis])
   p2=interpolate.PiecewisePolynomial(x2,y2[:,np.newaxis])
   def pdiff(x):
       return p1(x)-p2(x)
   xs=np.r_[x,x2]
   xs.sort()
   x_min=xs.min()
   x_max=xs.max()
   x_mid=xs[:-1]+np.diff(xs)/2
   roots=set()
   for val in x_mid:
       root,infodict,ier,mesg = optimize.fsolve(pdiff,val,full_output=True)
       # ier==1 indicates a root has been found
       if ier==1 and x_min<root<x_max:
           roots.add(root[0])
       #else:
        #  print ("No match point found")
   roots=list(roots)
   #print(np.column_stack(("%.2f" % roots[0],"%.2f" % p1(roots[0]))))
   #l = plt.axhline(linewidth=4, color='r')
   #l = plt.axhline(y=p1(roots[1]), xmin=0, xmax=0.1
   #print roots[0]
   #print sl_contrast
   #print ier
   #if ier == 1:
   l = plt.axhline(y=p1(roots[0]), xmin=0, xmax=(roots[0]/100))
   l = plt.axvline(x=roots[0], ymin=0, ymax=((p1(roots[0])/8)+0.125))
   l = plt.axhline(y=p1(roots[0]), xmin=0, xmax=(roots[0]/120))
   l = plt.axvline(x=roots[0], ymin=0, ymax=((p1(roots[0])/8)+0.125))
   plt.text(10, ((p1(roots[0]))+0.5), ( "Match point"), fontsize=15)
   plt.text(10, ((p1(roots[0]))+0.125), ( "%.2f" % roots[0], "%.2f" % p1(roots[0])), fontsize=15) 
   plt.legend([title, "Water"], bbox_to_anchor=(0.80, 0.3), loc=2, prop={'size':10}, borderaxespad=0.)
   plt.xlabel('% Deuteration')
   plt.ylabel('SLD *10$^{-6}\AA^{-2}$')

   imgdata = io.BytesIO()
   fig1.savefig(imgdata, format='png')
   imgdata.seek(0)  # rewind the data

   #print "Content-type: image/png\n"
   uri = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.buf))
   #print """/
   #<img height= height="600">
   #"""
   print('<img src = "%s"/ height="600" width="800">' % uri)

#else:
 #

print("""\
<p>
<a href="http://psldc.isis.rl.ac.uk/Psldc/index.html">Back to input page</a>
</p>
""")
