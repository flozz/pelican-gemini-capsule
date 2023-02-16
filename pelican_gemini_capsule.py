from pathlib import Path
from io import StringIO

import jinja2
import pelican
import rst2gemtext


GEMINI_NUMBER_ARTICLES_ON_HOME = 10


TEMPLATE_ARTICLE = """\
# {{ article.title }}
{{ article.date.strftime("%Y-%m-%d") }}

{{ article.content_gemtext }}

--------------------------------------------------------------------------------
=> {% if SITEURL %}{{ SITEURL }}{% else %}/{% endif %} 🏠 Home
"""

TEMPLATE_HOME = """\
# {{ SITENAME }}

## Latest Articles
{% for i in range(GEMINI_NUMBER_ARTICLES_ON_HOME) %}{% set article = articles[i] %}
=> {{ article.url | replace(".html", ".gmi") }} {{ article.date.strftime("%Y-%m-%d") }} {{ article.title -}}
{% endfor %}
{% if articles | length > GEMINI_NUMBER_ARTICLES_ON_HOME %}
=> {{ SITEURL }}all_articles.gmi ➕ All Articles
{% endif %}
"""

TEMPLATE_ALL_ARTICLES = """\
# All Articles — {{ SITENAME }}
{% for article in articles %}
=> {{ article.url | replace(".html", ".gmi") }} {{ article.date.strftime("%Y-%m-%d") }} {{ article.title -}}
{% endfor %}

--------------------------------------------------------------------------------
=> {% if SITEURL %}{{ SITEURL }}{% else %}/{% endif %} 🏠 Home
"""


def generate_article(generator, article, save_as):
    # Read and parse the reStructuredText file
    with open(article.source_path, "r") as rst_file:
        document = rst2gemtext.parse_rst(rst_file.read())

    # Remove first title from the document as it will be added back later using
    # the template
    node = document
    while True:
        node = node.next_node()
        if not node:
            break
        if node.tagname == "title":
            node.parent.remove(node)
            break

    # Convert the reStructuredText into Gemtext
    writer = rst2gemtext.GemtextWriter()
    gmi_io = StringIO()
    writer.write(document, gmi_io)
    gmi_io.seek(0)

    # Render the final Gemtext file (templating)
    article.content_gemtext = gmi_io.read()
    template = jinja2.Template(TEMPLATE_ARTICLE)
    rendered_article = template.render(generator.context, article=article)

    # Write the output file
    with open(save_as, "w") as gmi_file:
        gmi_file.write(rendered_article)


def generate_home_page(generator):
    save_as = Path(generator.output_path) / "index.gmi"

    # Render thepage (templating)
    template = jinja2.Template(TEMPLATE_HOME)
    rendered_page = template.render(
        generator.context,
        GEMINI_NUMBER_ARTICLES_ON_HOME=min(
            len(generator.articles), GEMINI_NUMBER_ARTICLES_ON_HOME
        ),
    )

    # Write the output file
    with open(save_as, "w") as gmi_file:
        gmi_file.write(rendered_page)


def generate_all_articles_page(generator):
    save_as = Path(generator.output_path) / "all_articles.gmi"

    # Render the page (templating)
    template = jinja2.Template(TEMPLATE_ALL_ARTICLES)
    rendered_page = template.render(generator.context)

    # Write the output file
    with open(save_as, "w") as gmi_file:
        gmi_file.write(rendered_page)


def article_generator_write_article(generator, content=None):
    save_as = Path(generator.output_path) / Path(content.save_as).with_suffix(".gmi")
    generate_article(generator, content, save_as)


def article_writer_finalized(generator, writer=None):
    generate_home_page(generator)
    generate_all_articles_page(generator)


def register():
    pelican.signals.article_generator_write_article.connect(
        article_generator_write_article
    )
    pelican.signals.article_writer_finalized.connect(article_writer_finalized)
