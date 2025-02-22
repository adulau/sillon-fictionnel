export TEXINPUTS=.:../static/:
python3 isbn.py --dump >full.md
pandoc  -V footnotes-pretty=true -V table-use-row-color=true -V toc-own-page=true --template=book.tex -s --highlight-style=tango --highlight-style=monochrome --resource-path ../static/:. --toc --pdf-engine=xelatex -f gfm full.md -o revue.pdf
#pandoc  --highlight-style=monochrome -V geometry:margin=1in --resource-path ../static/:. --toc --pdf-engine=xelatex -f gfm full.md -o revue.html
#rm -rf tmp-revue
#mkdir tmp-revue
#cp -rf ../content/post/*.md ./tmp-revue
#cp -rf ../static/images ./tmp-revue
#cd tmp-revue
#find . -type f -exec sed -i "/+++/,/+++/d" {} \;
#pandoc --verbose -f markdown --metadata lang:fr *.md -o revue.pdf --pdf-engine=xelatex
