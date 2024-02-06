import requests
from django.conf import settings

class DomainApi:

    
    @staticmethod
    def fetch_crawled_domains(domains):
        """
        Segregates a list of domains into visited and unvisited domains.
        
        Given a list of domains, this method sends a request to a designated ARTICLE_URL
        to check which domains have been crawled.
        
        Args:
        - domains (list): A list of dictionaries representing domains to be checked.
        
        Returns:
        - crawled_domains (list): List of crawled domains along with their crawlable and visited status.
        """
        article_url = settings.ARTICLE_URL + 'domains/check_crawled'
        data = {"urls" : domains}
        response = requests.post(article_url, json=data)
        crawled_domains = response.json()
        return crawled_domains
    
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
    def save_domains(domains):
        if not domains:
            return
        to_update = []
        to_create = []
        for domain in domains:
            if domain['visited']:
                to_create.append(domain)
                continue
            to_update.append(domain)
            
        article_url = settings.ARTICLE_URL + 'domains/check_crawled'
        data = {"urls" : domains}
        # response = requests.post(taks_url, json=data)
        # return response.json()