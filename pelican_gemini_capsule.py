from pathlib import Path
from io import StringIO

import jinja2
import pelican
import rst2gemtext


TEMPLATE_ARTICLE = """\
=> {% if SITEURL %}{{ SITEURL }}{% else %}/{% endif %} 🏠 {{ SITENAME }}

# {{ article.title }}
{{ article.date.strftime("%Y-%m-%d") }}

{{ article.content_gemtext }}
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


def article_generator_write_article(generator, content=None):
    save_as = Path(generator.output_path) / Path(content.save_as).with_suffix(".gmi")
    generate_article(generator, content, save_as)


def register():
    pelican.signals.article_generator_write_article.connect(
        article_generator_write_article
    )
