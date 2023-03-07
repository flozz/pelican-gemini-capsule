import html
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
=> {{ GEMSITEURL }}/{{ article.url | replace(".html", ".gmi") }} {{ article.date.strftime("%Y-%m-%d") }} {{ article.raw_title -}}
{% endfor %}
{% if articles | length > articles_count_on_home %}
=> {{ GEMSITEURL }}/all_articles.gmi ➕ All Articles
{% endif %}
"""

TEMPLATE_ARTICLES_INDEX_PAGE = """\
# All Articles — {{ SITENAME }}
{% for article in articles %}
=> {{ GEMSITEURL }}/{{ article.url | replace(".html", ".gmi") }} {{ article.date.strftime("%Y-%m-%d") }} {{ article.raw_title -}}
{% endfor %}

--------------------------------------------------------------------------------
=> {{ GEMSITEURL }}/ 🏠 Home
"""

TEMPLATE_ARTICLE = """\
# {{ article.raw_title }}
{{ article.date.strftime("%Y-%m-%d") }}

{{ article.content_gemtext }}

--------------------------------------------------------------------------------
=> {{ GEMSITEURL }}/ 🏠 Home
"""


class PelicanGemtextWriter(rst2gemtext.GemtextWriter):
    def __init__(self, generator, article):
        rst2gemtext.GemtextWriter.__init__(self)
        self._generator = generator  # Pelican generator
        self._article = article  # Pelican article

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

    def _clean_figure_links(self):
        def _loop_on_nodes(nodes):
            for node in nodes:
                if isinstance(node, rst2gemtext.NodeGroup) and not isinstance(
                    node, rst2gemtext.FigureNode
                ):
                    _loop_on_nodes(node.nodes)
                    continue
                if not isinstance(node, rst2gemtext.FigureNode):
                    continue
                if len(node.nodes) < 2:
                    continue
                if not isinstance(node.nodes[0], rst2gemtext.LinkNode):
                    continue
                if not isinstance(node.nodes[1], rst2gemtext.LinkNode):
                    continue
                if node.nodes[0].uri.endswith(node.nodes[1].uri) or node.nodes[
                    1
                ].uri.endswith(node.nodes[0].uri):
                    if node.nodes[0].uri == node.nodes[0].rawtext:
                        node.nodes.pop(0)
                    elif node.nodes[1].uri == node.nodes[1].rawtext:
                        node.nodes.pop(1)

        _loop_on_nodes(self.visitor.nodes)

    def _resolve_internal_links(self):
        def _loop_on_nodes(nodes):
            for node in nodes:
                if isinstance(node, rst2gemtext.NodeGroup):
                    _loop_on_nodes(node.nodes)
                    continue
                if not isinstance(node, rst2gemtext.LinkNode):
                    continue
                if not node.uri.startswith("{filename}"):
                    continue
                article_path = Path(self._article.source_path)
                target_path = (article_path.parent / node.uri[10:]).resolve()
                for article in self._generator.articles:
                    if target_path.as_posix() == article.source_path:
                        target_uri = Path("/%s" % article.url)
                        if target_uri.as_posix().endswith(
                            ".html"
                        ) or target_uri.as_posix().endswith(".htm"):
                            target_uri = target_uri.with_suffix(".gmi")
                        node.uri = target_uri.as_posix()
                        break

        _loop_on_nodes(self.visitor.nodes)

    def _before_translate_output_generation_hook(self):
        self._remove_first_title()
        self._remove_attach_tag_from_links()
        self._clean_figure_links()
        self._resolve_internal_links()


def generate_article(generator, article, save_as):
    template_text = generator.settings.get("GEMINI_TEMPLATE_ARTICLE", TEMPLATE_ARTICLE)

    # Read and parse the reStructuredText file
    with open(article.source_path, "r") as rst_file:
        document = rst2gemtext.parse_rst(rst_file.read(), rst_file.name)

    # Avoid HTML entities in titles
    article.raw_title = html.unescape(article.title)

    # Convert the reStructuredText into Gemtext
    writer = PelicanGemtextWriter(generator, article)
    gmi_io = StringIO()
    writer.write(document, gmi_io)
    gmi_io.seek(0)

    # Render the final Gemtext file (templating)
    article.content_gemtext = gmi_io.read()
    template = jinja2.Template(template_text)
    rendered_article = template.render(
        generator.context,
        article=article,
        GEMSITEURL=generator.settings.get("SITEURL", "")
        .replace("http://", "gemini://")
        .replace("https://", "gemini://"),
    )

    # Write the output file
    save_as.parent.mkdir(parents=True, exist_ok=True)
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
        GEMSITEURL=generator.settings.get("SITEURL", "")
        .replace("http://", "gemini://")
        .replace("https://", "gemini://"),
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
    rendered_page = template.render(
        generator.context,
        GEMSITEURL=generator.settings.get("SITEURL", "")
        .replace("http://", "gemini://")
        .replace("https://", "gemini://"),
    )

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
