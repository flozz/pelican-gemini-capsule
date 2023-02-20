from pathlib import Path
from io import StringIO

import jinja2
import pelican
import rst2gemtext


DISPLAYED_ARTICLE_COUNT_ON_HOME = 10

TEMPLATE_HOME = """\
# {{ SITENAME }}

## Latest Articles
{% for i in range(articles_count_on_home) %}{% set article = articles[i] %}
=> {{ article.url | replace(".html", ".gmi") }} {{ article.date.strftime("%Y-%m-%d") }} {{ article.title -}}
{% endfor %}
{% if articles | length > articles_count_on_home %}
=> {{ SITEURL }}all_articles.gmi ➕ All Articles
{% endif %}
"""

TEMPLATE_ARTICLES_INDEX_PAGE = """\
# All Articles — {{ SITENAME }}
{% for article in articles %}
=> {{ article.url | replace(".html", ".gmi") }} {{ article.date.strftime("%Y-%m-%d") }} {{ article.title -}}
{% endfor %}

--------------------------------------------------------------------------------
=> {% if SITEURL %}{{ SITEURL }}{% else %}/{% endif %} 🏠 Home
"""

TEMPLATE_ARTICLE = """\
# {{ article.title }}
{{ article.date.strftime("%Y-%m-%d") }}

{{ article.content_gemtext }}

--------------------------------------------------------------------------------
=> {% if SITEURL %}{{ SITEURL }}{% else %}/{% endif %} 🏠 Home
"""


class PelicanGemtextWriter(rst2gemtext.GemtextWriter):
    def _remove_first_title(self):
        for i in range(len(self.visitor.nodes)):
            node = self.visitor.nodes[i]
            if type(node) is rst2gemtext.TitleNode and node.level == 1:
                self.visitor.nodes.pop(i)
                break

    def _remove_attach_tag_from_links(self):
        def _loop_on_nodes(nodes):
            for node in nodes:
                if isinstance(node, rst2gemtext.NodeGroup):
                    _loop_on_nodes(node.nodes)
                elif isinstance(node, rst2gemtext.LinkNode):
                    if node.uri.startswith("{attach}"):
                        node.uri = node.uri[8:]
                    if node.rawtext.startswith("{attach}"):
                        node.rawtext = node.uri[8:]

        _loop_on_nodes(self.visitor.nodes)

    def _before_translate_output_generation_hook(self):
        self._remove_first_title()
        self._remove_attach_tag_from_links()


def generate_article(generator, article, save_as):
    template_text = generator.settings.get("GEMINI_TEMPLATE_ARTICLE", TEMPLATE_ARTICLE)

    # Read and parse the reStructuredText file
    with open(article.source_path, "r") as rst_file:
        document = rst2gemtext.parse_rst(rst_file.read())

    # Convert the reStructuredText into Gemtext
    writer = PelicanGemtextWriter()
    gmi_io = StringIO()
    writer.write(document, gmi_io)
    gmi_io.seek(0)

    # Render the final Gemtext file (templating)
    article.content_gemtext = gmi_io.read()
    template = jinja2.Template(template_text)
    rendered_article = template.render(generator.context, article=article)

    # Write the output file
    with open(save_as, "w") as gmi_file:
        gmi_file.write(rendered_article)


def generate_home_page(generator):
    save_as = Path(generator.output_path) / "index.gmi"
    template_text = generator.settings.get("GEMINI_TEMPLATE_HOME", TEMPLATE_HOME)
    articles_count_on_home = generator.settings.get(
        "GEMINI_DISPLAYED_ARTICLE_COUNT_ON_HOME", DISPLAYED_ARTICLE_COUNT_ON_HOME
    )

    # Render the page (templating)
    template = jinja2.Template(template_text)
    rendered_page = template.render(
        generator.context,
        articles_count_on_home=min(len(generator.articles), articles_count_on_home),
    )

    # Write the output file
    with open(save_as, "w") as gmi_file:
        gmi_file.write(rendered_page)


def generate_all_articles_page(generator):
    save_as = Path(generator.output_path) / "all_articles.gmi"
    template_text = generator.settings.get(
        "GEMINI_TEMPLATE_ARTICLES_INDEX_PAGE", TEMPLATE_ARTICLES_INDEX_PAGE
    )

    # Render the page (templating)
    template = jinja2.Template(template_text)
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
