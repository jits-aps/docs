import requests
import lxml.html
from lxml.html.clean import clean_html
import os
from shutil import rmtree, copy

class rst:
  """docstring for rst"""
  def __init__(self, url, title, hide_toc = True, recursive_render = True, parent = None):
    self.url = url
    self.title = title
    self.req = requests.get(self.url)
    self.html = self.req.text
    self.rst = ''
    self.toc = []
    self.hide_toc = hide_toc
    self.parent = parent
    self.children = []
    self.recursive = recursive_render
    self.output = ''
  
  def add_child(self, url, title, hide_toc = True, recursive_render = True):
    child = rst(url, title, hide_toc, recursive_render, parent = self)
    self.children.append(child)
    return child

  def render(self):
    self.output += '=' * len(self.title) + '\n'
    self.output += self.title + '\n'
    self.output += '=' * len(self.title) + '\n\n'

    self.output += self.rst + '\n\n'

    self.output += '.. toctree::\n'
    if self.hide_toc:
      self.output += '   :hidden:\n'
    self.output += '   \n'
    for line in self.toc:
      self.output += '   ' + line + '\n'
    self.output += '\n'

    if self.recursive:
      for i in self.children:
        i.render()


def traverse(el = [], dr = 'unknown', depth = 0):
  os.chdir(dr)
  text = '.. toctree::\n'
  if depth > 0:
    text += '   :hidden:\n'
  else:
    text = '=====\nIndex\n=====\n\n' + text
  text += '\n'
    
  for e in el:
    data = e.xpath('./a[@target="hmcontent"]/@href | ./a/span/text()')
    print(data)
    if any(i.tag == 'ul' for i in e.xpath('./*')):
      try:
        os.mkdir(data[0].replace('.htm', ''))
      except FileExistsError:
        pass
      index = data[0].replace('.htm', '') + '/index.htm'
      rsti = open(index.replace('.htm', '.rst'), 'w', encoding='utf-8')
      rsti.write('=' * len(data[-1]) + '\n')
      rsti.write(data[-1] + '\n')
      rsti.write('=' * len(data[-1]) + '\n\n')
      rsti.write('.. raw:: html\n')
      rsti.write('   :file: ' + index + '\n\n')
      rsti.close()
      traverse(e.xpath('./ul/li'), data[0].replace('.htm', ''), depth=depth+1) #Traverse all sublinks
    else:
      index = data[0]
    r = requests.get('http://www.admind.info/help/system6/' + data[0]) #html
    r.encoding = 'utf-8'
    f = open(index, 'w', encoding='utf-8')
    #f.write(strip_tags.sub('', remove_scripts.sub('', remove_styles.sub('', return_body.search(r.text).group(1)))))
    frgm = lxml.html.document_fromstring(r.text).xpath('//div[@id="innerdiv"]')[0]

    try:
      f.write(clean_html(lxml.html.tostring(frgm, encoding='unicode')))
    except:
      print(r.url)
    #f.write(r.text)
    f.close()                                                          #html
    
    text += '   ' + index.replace('.htm', '') + '\n'

    if not index.endswith('/index.htm'): #Write random files only containing title
      rst = open(index.replace('.htm', '.rst'), 'w', encoding='utf-8')
      rst.write('=' * len(data[1]) + '\n')
      rst.write(data[1] + '\n')
      rst.write('=' * len(data[1]) + '\n\n')
      rst.write('.. raw:: html\n')
      rst.write('   :file: ' + index + '\n\n')
      rst.close()

  rsti = open('index.rst', 'a', encoding='utf-8')
  rsti.write(text)
  rsti.close()
  os.chdir('..')


try:
  rmtree('data')
except FileNotFoundError:
  pass

doc = lxml.html.parse('http://www.admind.info/help/system6/hmcontent.htm').getroot()
try:
  os.mkdir('data')
except FileExistsError:
  pass

traverse(doc.xpath('//ul[@id="toc"]/li'), 'data')
#doc.make_links_absolute()
#open_in_browser(doc)

copy('rst/conf.py', 'data/conf.py')