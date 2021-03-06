Pelican BibTeX
==============

Organize your scientific publications with BibTeX in Pelican

Author of this fork: Jaime Arias (himito)
Original Author: Vlad Niculae (vene, https://github.com/vene/pelican-bibtex/)

*Note*: This code is unlicensed. It was not submitted to the `pelican-plugins`
official repository because of the license constraint imposed there.

History
=======

- Aug 3, 2013 (Vlad Niculae): Initial release of the pelican plugin.
- Jul 21, 2014 (Emmanuel Fleury): Added a few features and releasing version 0.3.
- Jan 19, 2016 (Jaime Arias): Refactoring code.


Requirements
============

`pelican_bibtex` requires `pybtex`.

```bash
pip install "pybtex==0.19"
```

How to Use
==========

This plugin reads a user-specified BibTeX file and populates the context with
a list of publications, ready to be used in your Jinja2 template.

Configuration is simply:

```python
PUBLICATIONS_SRC = 'content/pubs.bib'
```

If the file is present and readable, you will be able to find the `publications`
variable in all templates.  It is a list of dictionary  with the following keys:

```
{bibtex, doi, entry, text, url, note, year}
```

- `bibtex` is a string containing BibTeX code for the entry, useful to make it available to people who want to cite your work.
- `doi` is the DOI identification number.
- `entry` is the type of BibTeX entry is comes out as a couple with `(rank, label)`.
- `text` is the HTML formatted entry, generated by `pybtex`.
- `url` is the URL where to get the material or where to contact the publisher to get it.
- `note` is a custom note for the entry.
- `year` is the year when the entry was published.  Useful for grouping by year in templates using Jinja's `groupby`.
This plugin will take all defined fields and make them available in the template.

If a field is not defined, the tuple field will be `None`.  Furthermore, the
fields are stripped from the generated BibTeX (found in the `bibtex` field).


Template Example
================

You probably want to define a 'publications.html' direct template.
Don't forget to add it to the `DIRECT\_TEMPLATES` configuration key.
Note that we are escaping the BibTeX string twice in order to properly
display it.

```python
{% extends "base.html" %}
{% block title %}Publications{% endblock %}
{% block content %}

<section id="content" class="body">
  <div class="container">
    {% for group in publications|groupby('year')|reverse %}
        <h2>{{ group.grouper }}</h2>
        <ul>
          {% for publication in group.list|sort(attribute='year')|reverse %}
            <li>{{ publication.text }}</li>
          {% endfor %}
        </ul>
    {% endfor %}
  </div>
</section>
{% endblock %}
```

Extending this plugin
=====================

A relatively simple but possibly useful extension is to make it possible to
write internal links in Pelican pages and blog posts that would point to the
corresponding paper in the Publications page.

A slightly more complicated idea is to support general referencing in articles
and pages, by having some BibTeX entries local to the page, and rendering the
bibliography at the end of the article, with anchor links pointing to the right
place.
