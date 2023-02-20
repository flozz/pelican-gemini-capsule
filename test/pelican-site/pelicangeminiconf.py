# How many articles to display on the home page
GEMINI_DISPLAYED_ARTICLE_COUNT_ON_HOME = 10

# Template of the home page of the Gemlog
GEMINI_TEMPLATE_HOME = """\
# {{ SITENAME }}

## Latest Articles
{% for i in range(articles_count_on_home) %}{% set article = articles[i] %}
=> {{ article.url | replace(".html", ".gmi") }} {{ article.date.strftime("%Y-%m-%d") }} {{ article.title -}}
{% endfor %}
{% if articles | length > GEMINI_DISPLAYED_ARTICLE_COUNT_ON_HOME %}
=> {{ SITEURL }}all_articles.gmi ➕ All Articles
{% endif %}
"""

# Template of the "All Articles" page
GEMINI_TEMPLATE_ARTICLES_INDEX_PAGE = """\
# All Articles — {{ SITENAME }}
{% for article in articles %}
=> {{ article.url | replace(".html", ".gmi") }} {{ article.date.strftime("%Y-%m-%d") }} {{ article.title -}}
{% endfor %}

--------------------------------------------------------------------------------
=> {% if SITEURL %}{{ SITEURL }}{% else %}/{% endif %} 🏠 Home
"""

# Template of articles
GEMINI_TEMPLATE_ARTICLE = """\
# {{ article.title }}
{{ article.date.strftime("%Y-%m-%d") }}

{{ article.content_gemtext }}

--------------------------------------------------------------------------------
=> {% if SITEURL %}{{ SITEURL }}{% else %}/{% endif %} 🏠 Home
"""
