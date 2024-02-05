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
