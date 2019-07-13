# Script to generate index.html for the Github Pages site
# Run with Python 3
import markdown2
import sys
from jinja2 import Template

indexMarkDown = open("../../README.md", "r", encoding='utf8').read()
indexHtml = markdown2.markdown(indexMarkDown)

# index.html
f = open('./template/index.html.jinja2','r',encoding='utf-8')
t = Template(f.read())
f.close()
output = t.render(body = indexHtml)
f2 = open('../../build/index.html',"w", encoding='utf8')
f2.write(output)
f2.close()