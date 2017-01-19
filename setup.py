import pelican_bibtex
from distutils.core import setup

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: Public Domain
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development
Operating System :: POSIX
Operating System :: Unix

"""

LONG_DESCRIPTION = """\
Requirements
============

pelican\_bibtex requires pybtex.

This plugin reads a user-specified BibTeX file and populates the context with
a list of publications, ready to be used in your Jinja2 template.

If the file is present and readable, you will be able to find the 'publications'
variable in all templates. It is a dictionary with the following fields:

- bibtex: string containing the BibTex code for the entry.
- doi: doi number of the entry
- entry: type of the entry (book, incollection, etc.)
- text: parsed entry.
- url: url field of the entry
- note: note field of the entry
- year: year of publication of the entry

"""

setup(
    name='pelican_bibtex',
    description='Organize your scientific publications with BibTeX in Pelican',
    long_description=LONG_DESCRIPTION,
    version=pelican_bibtex.__version__,
    author='Vlad Niculae & Jaime Arias',
    author_email='jaime.arias@inria.fr',
    url='https://github.com/himito/pelican-bibtex',
    py_modules=['pelican_bibtex', 'style.mystyle'],
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    install_requires=[
        "pybtex==0.19",
    ],
)
