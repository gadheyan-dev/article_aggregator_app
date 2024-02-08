from bson import json_util
import tldextract
import json


def convert_urls_to_domain(urls, many=True):
    """
        Converts a given URL or a list of URLs to valid domains.

        Args:
            urls (str or list): The input URL or a list of URLs.
            many (bool): Whether the input is a single URL or a list of URLs.

        Returns:
            str or list: The extracted domain or a list of domains.

        Example:
        ```python
        url_example = "https://www.example.com/path/to/page"
        domains_single = convert_urls_to_domain(url_example, many=False)
        print(domains_single)
        # Output: 'https://www.example.com'

        urls_example = ["https://www.example1.com/path1", "https://www.example2.com"/path2]
        domains_multiple = convert_urls_to_domain(urls_example)
        print(domains_multiple)
        # Output: ['https://www.example1.com', 'https://www.example2.com']
        ```
        """
    urls = [urls] if not many else urls

    domains = []
    for url in urls:
        tld_info = tldextract.extract(url)
        scheme = "https"
        subdomain = tld_info.subdomain or "www"
        domain = f"{scheme}://{subdomain}.{tld_info.domain}.{tld_info.suffix}"
        domains.append(domain)

    return domains[0] if not many else domains


def split_into_visited_and_unvisited(input_domains, crawled_domains):
    """
    Segregates a list of domains into visited and unvisited domains.

    Given a list of domains, it separates the input 'input_domains'
    into two groups: 'crawled_domains' (visited) and 'uncrawled_domains' (unvisited).

    Args:
        - input_domains (list): A list of domains to be checked.
        - crawled_domains (list): A list of dictionaries representing crawled domains.

    Returns:
        - crawled_domains (list): List of crawled domains along with their crawlable and visited status.

    Example:
    ```python
    # Example Usage:
    input_domains = ["example1.com", "example2.com", "example3.com"]
    crawled_domains = [
        {'url': "example1.com", 'is_crawlable': True, 'visited': True},
        {'url': "example2.com", 'is_crawlable': False, 'visited': True}
    ]

    # Call the function to segregate domains
    resulting_crawled_domains = split_into_visited_and_unvisited(input_domains, crawled_domains)

    # Print the resulting crawled domains
    for domain_info in resulting_crawled_domains:
        print(domain_info)

    # Output:
    # {'url': 'example1.com', 'is_crawlable': True, 'visited': True}
    # {'url': 'example2.com', 'is_crawlable': False, 'visited': True}
    # {'url': 'example3.com', 'is_crawlable': True, 'visited': False}

    # The function adds unvisited domains from input_domains to crawled_domains
    # while setting 'is_crawlable' to True and 'visited' to False.
    ```
    """
    visited_domains_tracker = set()

    for domain_obj in crawled_domains:
        visited_domains_tracker.add(domain_obj['url'])

    for domain in input_domains:
        if domain not in visited_domains_tracker:
            current_domain = {'url': domain,
                              'is_crawlable': True, 'visited': False}
            crawled_domains.append(current_domain)

    return crawled_domains
