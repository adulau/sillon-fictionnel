#!/bin/bash
# 
# Generating the book from the sillon-fictionnel.club
#
# The process is quite simple
# 
# - Two markdown files entete.md and apropos.md are the headers of the global markdown file
# - A generic script is used to generate the markdown file from all the post of the sillon-fictionnel.club
# - then pandoc with the eisvogel template and some lua script is used to convert the markdown to LateX then to PDF
#
# Additional notes:
# 
# If you have any issue with the EB Garamond font especially the WOFF files.
#
# Get rid of the incorrect WOFF from fontconfig by creating an exclusion file
# in /etc/fonts/conf.d/70-no-woff.conf
#
# <fontconfig>
# <!-- Reject WOFF fonts We don't register WOFF(2) fonts with fontconfig because of the W3C spec -->
#  <selectfont>
#  <rejectfont>
#   <glob>/usr/share/fonts/woff/*</glob>
#  </rejectfont>
# </selectfont>
# </fontconfig>
#
# This bricolage has been written by Alexandre Dulaunoy while listening to Pasillo, Montoya which could explain the
# result of the code and the overall script.
#

export TEXINPUTS=.:../static/:
cat entete.md >full.md
cat apropos.md >>full.md
python3 isbn.py --dump >>full.md
pandoc  --lua-filter=revue.lua -V book=true -V colorlinks=true -V linkcolor=blue  -V urlcolor=red -V toccolor=gray -V lang=fr -V footnotes-pretty=true -V table-use-row-color=true -V toc-own-page=true --template=eisvogel -s --highlight-style=tango --highlight-style=monochrome --resource-path ../static/:. --toc --pdf-engine=xelatex -f gfm full.md -o revue.pdf
scp revue.pdf ubuntu@sillon-fictionnel.club:/var/www/sillon-fictionnel.club/le-sillon-revue.pdf
