from rest_framework.exceptions import APIException

class ServiceUnavailableException(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class WebsiteNotReachableException(APIException):
    status_code = 503
    default_detail = 'Website is not reachable, try again later.'
    default_code = 'website_not_reachable'



class CrawlNotAllowedException(APIException):
    status_code = 403
    default_detail = 'Crawling is not allowed on this website.'
    default_code = 'crawl_not_allowed'

