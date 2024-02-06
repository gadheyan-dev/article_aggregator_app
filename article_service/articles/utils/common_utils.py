from bson import json_util
import tldextract
import json

"""
Extracts the domain from a given URL.
Args:
    url (str): The input URL.
Returns:
    str: The extracted domain.
"""
def convert_urls_to_domain(urls, many=True):
    domains = []
    if not many:
        urls = [urls]
    for url in urls:
        tld = tldextract.extract(url)
        scheme = "https"
        if not tld.subdomain:
            tld.subdomain = "www"
        domains.append(f"{scheme}://{tld.subdomain}.{tld.domain}.{tld.suffix}")

    if not many:
       domains = domains[0]

    return domains

def split_into_visited_and_unvisited(input_domains, crawled_domains):
    """
    Segregates a list of domains into visited and unvisited domains.
    
    Given a list of domains, it separates the input 'domains' 
    into two groups: 'crawled_domains' (visited) and 'uncrawled_domains' (unvisited).
    
    Args:
    - domains (list): A list of dictionaries representing domains to be checked.
    
    Returns:
    - crawled_domains (list): List of crawled domains along with their crawlable and visited status.
    """
    visited_domains_tracker = set()
    for domain_obj in crawled_domains:
        visited_domains_tracker.add(domain_obj['url'])
    
    for domain in input_domains:
        if domain not in visited_domains_tracker:
            current_domain = {'url':domain, 'is_crawlable':True, 'visited':False}
            crawled_domains.append(current_domain)

    return crawled_domains