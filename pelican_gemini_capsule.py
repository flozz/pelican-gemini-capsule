from pathlib import Path

from pelican import signals
import rst2gemtext


def article_generator_write_article(generator, content=None):
    article = content
    save_as = Path(generator.output_path) / Path(article.save_as).with_suffix(".gmi")
    with open(article.source_path, "r") as rst_file:
        document = rst2gemtext.parse_rst(rst_file.read())
    writer = rst2gemtext.GemtextWriter()
    with open(save_as, "w") as gmi_file:
        writer.write(document, gmi_file)


def register():
    signals.article_generator_write_article.connect(article_generator_write_article)
