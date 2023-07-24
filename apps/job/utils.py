from django.contrib.postgres.search import TrigramSimilarity

def compute_similarity(field_name, values):
    total_similarity = 0
    num_values = len(values)
    if num_values == 0:
        return 0  # Return 0 if there are no user_skills
    for value in values:
        total_similarity += TrigramSimilarity(field_name, value)
    return total_similarity / num_values