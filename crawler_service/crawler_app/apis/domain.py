import requests
from django.conf import settings


class DomainApi:

    @staticmethod
    def fetch_crawled_domains(domains):
        article_url = settings.ARTICLE_URL + 'domains/check_crawled'
        data = domains
        response = requests.post(article_url, json=data)
        crawled_domains = response.json()
        return crawled_domains

    @staticmethod
    def crawl_domains(domains):
        if not domains:
            return
        taks_url = settings.TASK_URL + 'tasks/crawl/'
        data = domains
        response = requests.post(taks_url, json=data)
        return response.json()

    @staticmethod
    def save_domains(domains):
        if not domains:
            return None

        to_update = [domain for domain in domains if domain['visited']]
        to_create = [domain for domain in domains if not domain['visited']]

        url = settings.ARTICLE_URL + 'domains/'
        response_create = None
        response_update = None
        if to_create:
            response_create = requests.post(url, json=to_create)
        if to_update:
            response_update = requests.put(url, json=to_update)

        return response_create, response_update

    @staticmethod
    def save_outbound_domains(domains):
        if not domains:
            return None
        list_of_domains = set()
        outbound_domains = {}
        unvisited_inbound_domains = []
        visited_inbound_domains = []
        for domain_obj in domains:
            for outbound_domain_url in domain_obj['outbound_domains']:
                list_of_domains.add(outbound_domain_url)
                if outbound_domain_url not in outbound_domains:
                    outbound_domains[outbound_domain_url] = {"url":outbound_domain_url, "inbound_domains":[]}
                outbound_domains[outbound_domain_url]["inbound_domains"].append(domain_obj['url'])
        list_of_domains = {"urls":list(list_of_domains)}
        visited_domains = DomainApi.fetch_crawled_domains(list_of_domains)
        for domain in visited_domains:
            domain["inbound_domains"] = outbound_domains[domain["url"]]["inbound_domains"]
            if not domain["visited"]:
                unvisited_inbound_domains.append(domain) 
                continue
            visited_inbound_domains.append(domain)
        url = settings.ARTICLE_URL + 'domains/'
        response_create = None
        response_patch = None
        if unvisited_inbound_domains:
            response_create = requests.post(url, json=unvisited_inbound_domains)
        if visited_inbound_domains:
            response_patch = requests.patch(url, json=visited_inbound_domains)

        return response_create, response_patch
