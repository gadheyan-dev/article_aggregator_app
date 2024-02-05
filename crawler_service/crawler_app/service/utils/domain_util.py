import requests
from django.conf import settings

class DomainUtil:

    @staticmethod
    def validate_domains(domains):
        article_url = settings.ARTICLE_URL + 'domains/check_crawled'
        domains = list(domains)
        data = {"urls" : domains}
        response = requests.post(article_url, json=data)
        visited_domains = response.json()
        visted_domain_tracker = set(visited_domains)
        for domain in domains:
            if domain not in visted_domain_tracker:
                visited_domains.append(domain)
        return visited_domains
    
    @staticmethod
    def crawl_domains(domains):
        if not domains:
            return
        taks_url = settings.TASK_URL + 'tasks/crawl/'
        data = {"urls" : domains}
        response = requests.post(taks_url, json=data)
        return response.json()
    
    @staticmethod
    def parse_feeds(feeds):
        if not feeds:
            return
        taks_url = settings.TASK_URL + 'tasks/parse_feeds/'
        data = {"feeds" : feeds}
        response = requests.post(taks_url, json=data)
        return response.json()

        
    @staticmethod
    def save_domains(feeds):
        if not feeds:
            return
        taks_url = settings.TASK_URL + 'tasks/parse_feeds/'
        data = {"feeds" : feeds}
        response = requests.post(taks_url, json=data)
        return response.json()