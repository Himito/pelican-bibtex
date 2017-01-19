"""
Pelican BibTeX
==============

A Pelican plugin that populates the context with a list of formatted
citations, loaded from a BibTeX file at a configurable path.
"""

# Fork author: Jaime Arias <jaime.arias@inria.fr>
# Initial author: Vlad Niculae <vlad@vene.ro>
# Unlicensed (see UNLICENSE for details)


from pelican import signals
from logging import getLogger

__version__ = '0.3'

LOGGER = getLogger(__name__)


def get_field(entry, field):
    """
    Get a field in an entry.
    """
    return entry.fields.get(field, "")


def add_publications(generator):
    """
    Populates context with a list of BibTeX publications.

    Configuration
    -------------
    generator.settings['PUBLICATIONS_SRC']:
        local path to the BibTeX file to read.

    Output
    ------
    generator.context['publications']:
        List of dictionaries with keys (bibtex, doi, entry, text, url, note,
        year). See Readme.md for more details.
    """
    if 'PUBLICATIONS_SRC' not in generator.settings:
        return

    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    try:
        from pybtex.database.input.bibtex import Parser
        from pybtex.database.output.bibtex import Writer
        from pybtex.database import BibliographyData, PybtexError
        from pybtex.backends import html
        from .style.mystyle import Style
    except ImportError:
        LOGGER.warn('`pelican_bibtex` failed to load dependency `pybtex`')
        return

    try:
        bib_items = Parser().parse_file(generator.settings['PUBLICATIONS_SRC'])
    except PybtexError as err:
        LOGGER.warn('`pelican_bibtex` failed to parse file %s: %s',
                    generator.settings['PUBLICATIONS_SRC'],
                    str(err))
        return

    publications = []

    for fmt_entry in Style().format_entries(bib_items.entries.values()):
        key = fmt_entry.key
        entry = bib_items.entries[key]

        # Render the bibtex string for the entry
        buf = StringIO()
        Writer().write_stream(BibliographyData(entries={key: entry}), buf)

        # Prettify BibTeX entries
        text = fmt_entry.text.render(html.Backend())
        text = text.replace(r"\{", "").replace(r"\}", "")
        text = text.replace("{", "").replace("}", "")

        publications.append({
            'bibtex': buf.getvalue(),
            'doi': get_field(entry, 'doi'),
            'entry': entry.type,
            'text': text,
            'url': get_field(entry, 'url'),
            'note': get_field(entry, 'note'),
            'year': entry.fields.get('year'),
        })

    generator.context['publications'] = publications


def register():
    """
    Register the signal to the Pelican framework.
    """
    signals.generator_init.connect(add_publications)
