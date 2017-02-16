This is a little tool to find freely available, open-access PDFs for articles
in a Bibtex file, and to alter the Bibtex file so that it points to these PDF
files.

The tool is quite specific to the use-case I had, but the included functions
might be useful in other contexts.

It requires an installation of `requests`
(https://github.com/kennethreitz/requests/) and `bibtexparser`
(https://github.com/sciunto-org/python-bibtexparser)

Here's what it does when executed as a script (change `SOURCE_FILENAME` and
`TARGET_FILENAME` in the source code directly to adapt to your system):

1. Go through the Bibtex file and check for each entry whether it has an URL
   with a Pubmed link (`http://www.ncbi.nlm.nih.gov/pubmed/...`)
2. Check whether [PubMedCentral](https://www.ncbi.nlm.nih.gov/pmc/) has a PDF
   for this article (following up redirections if necessary)
3. If yes, replace the URL in the Bibtex file with the URL to the PDF; if no,
   delete the URL (if we have a link to the article via the DOI field)

Please note that I am not particularly interested in extending this into a
fully-featured package that does a lot more than that. This was mostly a
one-use script that I am sharing just in case it is useful to anyone.

