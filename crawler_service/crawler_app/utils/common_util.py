
def join_lists(list1, list2, on="url", items_to_add=["keywords"]):
    result = []

    # Create a dictionary for faster lookups based on the specified "on" field in list2
    dict_key = lambda item: item[on]
    url_dict = {dict_key(item): item for item in list2}

    # Iterate through list1 and combine with matching values from list2
    for item1 in list1:
        join_value = item1[on]
        if join_value in url_dict:
            combined_item = {**item1, **{item: url_dict[join_value][item] for item in items_to_add}}
            result.append(combined_item)

    return result