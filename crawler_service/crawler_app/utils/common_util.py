
import requests

def is_website_reachable(url):
    try:
        response = requests.get(url)
        return response.status_code >= 200 and response.status_code < 300
    except requests.RequestException:
        return False
    
def join_lists(list1, list2, on="url", items_to_add=["keywords"]):
    result = []
    if not list2:
        return list1
    dict_key = lambda item: item[on]
    url_dict = {dict_key(item): item for item in list2}

    for item1 in list1:
        join_value = item1[on]
        if join_value in url_dict:
            combined_item = {**item1, **{item: url_dict[join_value][item] for item in items_to_add}}
            result.append(combined_item)

    return result