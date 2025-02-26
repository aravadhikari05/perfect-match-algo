from itertools import combinations
import pandas as pd

#TODO add more exclusions and implement generate matches

#First create score between 2 users(higher score = better match). Normalize?

def calculate_score(user1, user2):
    # -----junk gpt code - change after we get data -----

    # 1. Common interests (higher = better match)
    common_interests = len(set(user1["interested_in_majors"]) & set(user2["interested_in_majors"]))
    
    # 2. Age similarity (if 'prefers_same_age' is enabled)
    age_difference = abs(user1["age"] - user2["age"])
    age_score = 1 if (user1["prefers_same_age"] and user2["prefers_same_age"] and age_difference <= 2) else 0
    
    # 3. Personality Score Difference (smaller difference = better match)
    personality_difference = abs(user1["personality_score"] - user2["personality_score"])
    personality_score = 1 - personality_difference  # Normalize to 0-1 scale


    # Weighted score calculation
    match_score = (2 * common_interests) + (1.5 * age_score) + (2 * personality_score)
    
    #-----------------------------------------------------
    # TODO Normalize? - DONE
    max_score = 5.5 #arbitrary number
    normalized_score = raw_score/max_score
    return f' max_score: {max_score}'
    return f'normalized_score: {normalize_score} '

#Above function is O(n^2) - need exclusions
#Next create matches scores for each combination of 2 users (minus exceptions)

def generate_match_scores(data):
    matches = []

    user_list = data.to_dict(orient="records")

    for user1, user2 in combinations(user_list, 2):

        #Exclusions:

        #List of potential exclusions: 
        #gender doesn't match preferred gender, age doesnt match preferred age range, race?, religion?

        #1. If gender not in preferred genders. 
        if (user1["gender"] not in user2["preferences"].get("preferred_genders", []) or
            user2["gender"] not in user1["preferences"].get("preferred_genders", [])):
            continue #skips to next iteration

        #2.Location (if different locations, no match -> for now can change depending on maybe distance, etc)
        if user1['location'] != user2['location']:
            continue
        #3 If age doesnt match preferred age range
        if user2 not in user1['age'].get('age_range'):
            continue


        score = calculate_score(user1, user2)
        
        # Store the match if it passes filters
        matches.append({
            "user1": user1["name"],
            "user2": user2["name"],
            "match_score": score
        })


    scores = pd.DataFrame(matches)
    #scores = scores.sort_values(by="match_score", ascending=False)
    #scores.to_csv("filtered_match_results.csv", index=False)

    return scores



#Third, create a simple matching algorithm (this is temporary, will be improved later):
#When creating matches, each user can get a garuntee of 2 matches, and more matches get added onto a users match list
#Example, user 1s highest match scores are with (user 2 and user 3) but user 2s highest scores are with (user 4 and user 5).
#then user 1 will have user 2 and user 3 as matches, and user 2 will have user 4, user 5, AND user 1 as matches.

#idea is to create dictionary of matches for each user. 
# key will be user and the value will be a list of matches for that user

#things to consider is how many matches garunteed per user (3?), other potential algorithms

#mutual vs non-mutual matching system(from gpt)
def generate_matches(scores):
    scores = {}
    for user1, user2 in combinations(users, 2):
        score = calculate_score(user1, user2)
        scores[(user1["id"], user2["id"])] = score
        scores[(user2["id"], user1["id"])] = score
    
    # Store each user's top matches
    user_matches = {user["id"]: [] for user in users}
    for user in users:
        user_id = user["id"]
        
    # Get the top N matches for each user
        top_matches = sorted(
            [(other_id, score) for (u, other_id), score in scores.items() if u == user_id],
            key=lambda x: x[1],
            reverse=True
            )[:top_n]
        
        # Store the match list for this user
        user_matches[user_id] = [match[0] for match in top_matches]
    
    return user_matches
