import sphinx_rtd_theme
#import t3SphinxThemeRtd

extensions = [
  "sphinx_rtd_theme",
#  "t3SphinxThemeRtd"
]

html_theme = "sphinx_rtd_theme"

html_theme_options = {
  'collapse_navigation': False
}

#html_theme = "t3SphinxThemeRtd"
#html_theme_path = [t3SphinxThemeRtd.get_html_theme_path()]

project = "Admind"
primary_domain = "rst"