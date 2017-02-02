import logging

import requests
import bibtexparser

TOOLNAME = 'pubmed_pdf'
EMAIL = 'your_email@example.com'  # Please set if you use this extensively

API_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool={toolname}&email={email}&ids={pmid}&versions=no&format=json"
PMC_URL = "https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"

logging.basicConfig()
logger = logging.getLogger('pubmed_pdf')

def find_url(url):
    r = requests.head(url, headers={'User-Agent': 'fetch_pmc_pdf/0.1'})
    if r.status_code == 200:
        return url
    elif r.status_code == 303:  # redirect
        return find_url(r.headers['Location'])
    else:
        return None


def find_pmc_pdf(pmid):
    pmcid = pubmed_to_pmc(pmid)
    if pmcid is not None:
        logger.debug('PMCID: %s', pmcid)
        # Check whether PMC has a pdf
        url = PMC_URL.format(pmcid=pmcid[3:], toolname=TOOLNAME,
                             email=EMAIL)
        url = find_url(url)
        return url
    return None


def pubmed_to_pmc(pmid):
    url = API_URL.format(pmid=pmid, toolname=TOOLNAME, email=EMAIL)
    reply = requests.get(url).json()
    records = reply['records'][0]
    return records.get('pmcid', None)


def replace_pubmed_pmc(filename, new_filename=None, remove_links=False):
    if new_filename is None:
        new_filename = filename
    with open(filename) as f:
        bibtex = bibtexparser.load(f)
    counter = 0
    for entry in bibtex.entries:
        logger.info('Processing entry with title: ' + entry.get('title', '<Unknown>'))
        if entry.get('link', '').startswith('http://www.ncbi.nlm.nih.gov/pubmed/'):
            pmid = entry['link'][35:]
            logger.debug('Pubmed ID is %s', pmid)
            url = find_pmc_pdf(pmid)
            if url is not None:
                entry['link'] = url
                counter += 1
                logger.info('Found a PDF on PubMedCentral: %s', url)
            elif remove_links and 'doi' in entry:
                # Store the pubmed id but remove the link
                entry['pmid'] = str(pmid)
                del entry['link']
        if 'link' in entry:
            entry['url'] = entry['link']
            del entry['link']
    logger.info('Found entries for {counter}/{all} '
                 'entries'.format(counter=counter, all=len(bibtex.entries)))
    with open(new_filename, 'w') as f:
        bwriter = bibtexparser.bwriter.BibTexWriter()
        bwriter.order_entries_by = ('year', 'month')
        bibtexparser.dump(bibtex, f, bwriter)


if __name__ == '__main__':
    SOURCE_FILENAME = 'somefile.bib'
    TARGET_FILENAME = 'newfile.bib'
    logger.setLevel(logging.INFO)
    replace_pubmed_pmc(SOURCE_FILENAME, TARGET_FILENAME, remove_links=True)
