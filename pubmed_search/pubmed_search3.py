from metapub import PubMedFetcher
fetch = PubMedFetcher()
pmids = fetch.pmids_for_query("cancer", retmax=10)
for pmid in pmids:
    article = fetch.article_by_pmid(pmid)
    print(f"PMID: {pmid}, 摘要: {article.abstract}")