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
    def parse_feeds(feeds):
        if not feeds:
            return
        taks_url = settings.TASK_URL + 'tasks/parse_feeds/'
        data = {"feeds" : feeds}
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