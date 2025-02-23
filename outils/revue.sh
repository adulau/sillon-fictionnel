export TEXINPUTS=.:../static/:
python3 isbn.py --dump >full.md
#pandoc  --highlight-style=monochrome -V geometry:margin=1in --resource-path ../static/:. --toc --pdf-engine=xelatex -f gfm full.md -o revue.html
#pandoc  -V footnotes-pretty=true -V table-use-row-color=true -V toc-own-page=true --template=book.tex -s --highlight-style=tango --highlight-style=monochrome --resource-path ../static/:. --toc --pdf-engine=xelatex -f gfm full.md -o revue.pdf
pandoc  --lua-filter=revue.lua -V book=true -V colorlinks=true -V linkcolor=blue  -V urlcolor=red -V toccolor=gray -V lang=fr -V footnotes-pretty=true -V table-use-row-color=true -V toc-own-page=true --template=eisvogel -s --highlight-style=tango --highlight-style=monochrome --resource-path ../static/:. --toc --pdf-engine=xelatex -f gfm full.md -o revue.pdf
