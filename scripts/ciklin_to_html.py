# Script to generate index.html for the Github Pages site
# Run with Python 3
import markdown2
import sys
from jinja2 import Template

cikLinMarkDown = open("../CikLinBekIn.md", "r", encoding='utf8').read()
cikLinHtml = markdown2.markdown(cikLinMarkDown)

# CikLinBekIn.html
f = open('./template/ciklinbekin.html.jinja2','r',encoding='utf-8')
t = Template(f.read())
f.close()
output = t.render(body = cikLinHtml)
f2 = open('../build/CikLinBekIn.html',"w", encoding='utf8')
f2.write(output)
f2.close()