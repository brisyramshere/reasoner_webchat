import requests
import xml.etree.ElementTree as ET
def pubmed_search(keyword):
    # 步骤 1：使用 ESearch 获取 PMID 列表
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params = {
        "db": "pubmed",
        "term": keyword,
        "retmax": 10,  # 限制返回 10 篇论文，可调整
        "retmode": "json"
    }
    response = requests.get(esearch_url, params=esearch_params)
    data = response.json()
    pmids = data["esearchresult"]["idlist"]
    print(f"找到 {len(pmids)} 篇论文: {pmids}")

    # 步骤 2：使用 EFetch 获取摘要
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    efetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),  # 将 PMID 列表转为逗号分隔的字符串
        "retmode": "xml"
    }
    response = requests.get(efetch_url, params=efetch_params)
    xml_data = response.text

    # 解析 XML 并提取摘要
    root = ET.fromstring(xml_data)
    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text
        abstracts = article.findall(".//AbstractText")
        abstract_text = ""
        for abstract in abstracts:
            abstract_text += abstract.text + "\n"
        print(f"PMID: {pmid}")
        print(f"标题: {title}")
        print(f"摘要: {abstract_text}\n")