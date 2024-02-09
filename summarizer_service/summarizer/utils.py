def convert_rank_to_score(keyword_obj):
    min_rank = min(keyword["rank"] for keyword in keyword_obj["keywords"])
    max_rank = max(keyword["rank"] for keyword in keyword_obj["keywords"])

    def convert_single_rank(rank):
        # Assuming the rank can be any numeric value
        normalized_rank = (rank - min_rank) / (max_rank - min_rank)  # Normalize to [0, 1]
        return round(normalized_rank * 10, 2)

    # Add the 'score' key to each keyword entry
    for keyword in keyword_obj["keywords"]:
        keyword["score"] = convert_single_rank(keyword["rank"])

    return keyword_obj