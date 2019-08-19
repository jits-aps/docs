import requests
from lxml.etree import LXML_VERSION

html_theme = 'sphinx_rtd_theme'
html_style = None

html_theme_options = {
  'collapse_navigation': False
}

project = "Admind"
primary_domain = "rst"

master_doc = "index"

# These folders are copied to the documentation's HTML output
html_static_path = ['../_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/mod.css',
]

print('Requests: ' + requests.__version__)
print('LXML: ' + LXML_VERSION)
