from Bio import Entrez
import time
from urllib.error import URLError

Entrez.email = ""  # NCBI 要求提供邮箱
Entrez.api_key = ""
keyword = "cancer"

delay = 1
max_retries = 3

for attempt in range(3):
    try:
        # 搜索文章
        handle = Entrez.esearch(db="pubmed", term=keyword, retmax=10)
        result = Entrez.read(handle)
        pmids = result["IdList"]
        
        for pmid in pmids:
            try:
                # 获取文章详情
                handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
                record = Entrez.read(handle)
                article = record["PubmedArticle"][0]["MedlineCitation"]["Article"]
                
                # 获取标题和摘要
                title = article["ArticleTitle"]
                abstracts = article.get("Abstract", {}).get("AbstractText", ["No abstract available"])
                abstract_str = ""
                for abstract in abstracts:
                    abstract_str += str(abstract) + "\n"

                print(f"\nPMID: {pmid}")
                print(f"标题: {title}")
                print(f"摘要: {abstract_str}")
                print("-" * 80)
                
            except Exception as e:
                print(f"获取PMID {pmid} 的详情时出错: {str(e)}")
            
            time.sleep(delay)  # 在请求之间添加延迟
        
        break  # 如果成功则退出循环
        
    except URLError as e:
        if attempt < max_retries - 1:
            print(f"尝试 {attempt + 1} 失败，等待后重试...")
            time.sleep(delay * (attempt + 1))  # 增加重试延迟
        else:
            print(f"最终尝试失败: {str(e)}")
            raise