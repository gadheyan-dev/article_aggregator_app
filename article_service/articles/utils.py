from bson import json_util
import tldextract
import json

def parse_json(data):
    return json.loads(json_util.dumps(data))

"""
Extracts the domain from a given URL.
Args:
    url (str): The input URL.
Returns:
    str: The extracted domain.
"""
def get_domain_from_url(url):
    tld = tldextract.extract(url)
    domain = f"{tld.domain}.{tld.suffix}"
    return domain