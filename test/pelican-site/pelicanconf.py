import glob

AUTHOR = "Fabien LOISON"
SITENAME = "Pelican Test Site"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "en"

# Enable our plugin
PLUGINS = [
    "pelican_gemini_capsule",
]

# Static files
STATIC_PATHS = [
    path[len(PATH) + 1 :]
    for path in glob.glob("%s/**/images" % PATH, recursive=True)
    + glob.glob("%s/**/videos" % PATH, recursive=True)
    + glob.glob("%s/**/static" % PATH, recursive=True)
]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 4

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
