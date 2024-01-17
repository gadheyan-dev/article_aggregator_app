import tldextract


class URLUtil:
    url = ""

    def get_domain(url):
        extracted_info = tldextract.extract(url)
        subdomain = extracted_info.subdomain
        domain = extracted_info.domain
        tld = extracted_info.suffix
        subdomain = 'www' if not subdomain else subdomain
        full_domain = '.'.join(filter(None, [subdomain, domain, tld]))
        return full_domain
        
