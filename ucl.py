


import random
import collections

# Data for the 2025/26 UEFA Champions League Draw
LEAGUE_TEAMS = {
    # Pot 1
    "Paris Saint-Germain": {"country": "France", "pot": 1, "opponents": []},
    "Real Madrid": {"country": "Spain", "pot": 1, "opponents": []},
    "Bayern Munich": {"country": "Germany", "pot": 1, "opponents": []},
    "Inter Milan": {"country": "Italy", "pot": 1, "opponents": []},
    "Manchester City": {"country": "England", "pot": 1, "opponents": []},
    "Liverpool": {"country": "England", "pot": 1, "opponents": []},
    "Borussia Dortmund": {"country": "Germany", "pot": 1, "opponents": []},
    "Barcelona": {"country": "Spain", "pot": 1, "opponents": []},
    "Chelsea": {"country": "England", "pot": 1, "opponents": []},
    # Pot 2
    "Arsenal": {"country": "England", "pot": 2, "opponents": []},
    "Bayer Leverkusen": {"country": "Germany", "pot": 2, "opponents": []},
    "Atlético Madrid": {"country": "Spain", "pot": 2, "opponents": []},
    "Benfica": {"country": "Portugal", "pot": 2, "opponents": []},
    "Atalanta": {"country": "Italy", "pot": 2, "opponents": []},
    "Villarreal": {"country": "Spain", "pot": 2, "opponents": []},
    "Juventus": {"country": "Italy", "pot": 2, "opponents": []},
    "Eintracht Frankfurt": {"country": "Germany", "pot": 2, "opponents": []},
    "Club Brugge": {"country": "Belgium", "pot": 2, "opponents": []},
    # Pot 3
    "Tottenham Hotspur": {"country": "England", "pot": 3, "opponents": []},
    "PSV Eindhoven": {"country": "Netherlands", "pot": 3, "opponents": []},
    "Ajax": {"country": "Netherlands", "pot": 3, "opponents": []},
    "Napoli": {"country": "Italy", "pot": 3, "opponents": []},
    "Sporting CP": {"country": "Portugal", "pot": 3, "opponents": []},
    "Olympiacos": {"country": "Greece", "pot": 3, "opponents": []},
    "Slavia Prague": {"country": "Czechia", "pot": 3, "opponents": []},
    "Bodø/Glimt": {"country": "Norway", "pot": 3, "opponents": []},
    "Marseille": {"country": "France", "pot": 3, "opponents": []},
    # Pot 4
    "Copenhagen": {"country": "Denmark", "pot": 4, "opponents": []},
    "Monaco": {"country": "France", "pot": 4, "opponents": []},
    "Galatasaray": {"country": "Turkey", "pot": 4, "opponents": []},
    "Union Saint-gilloise": {"country": "Belgium", "pot": 4, "opponents": []},
    "Qarabağ": {"country": "Azerbaijan", "pot": 4, "opponents": []},
    "Athletic Club": {"country": "Spain", "pot": 4, "opponents": []},
    "Newcastle United": {"country": "England", "pot": 4, "opponents": []},
    "Pafos": {"country": "Cyprus", "pot": 4, "opponents": []},
    "Kairat Almaty": {"country": "Kazakhstan", "pot": 4, "opponents": []},
}

def reset_draw(teams):
    """Clears all opponent lists to prepare for a new draw attempt."""
    for team_name in teams:
        teams[team_name]["opponents"] = []

def perform_draw(teams):
    """
    Attempts to perform a full Champions League draw by filling one match slot at a time.
    This approach is more robust and avoids deadlocks caused by the tight constraints.
    """
    # Create a master list of all 288 individual match slots that need to be filled.
    # (36 teams * 8 opponents each)
    match_slots = []
    for team_name in teams.keys():
        for target_pot in range(1, 5):
            # Each team needs 2 opponents from each pot.
            match_slots.append((team_name, target_pot))
            match_slots.append((team_name, target_pot))
    
    random.shuffle(match_slots)

    for team_name, target_pot in match_slots:
        team_data = teams[team_name]
        
        # Check if this team's quota for the target pot is already full.
        opponents_from_pot = [opp for opp in team_data["opponents"] if teams[opp]["pot"] == target_pot]
        if len(opponents_from_pot) >= 2:
            continue

        # Find a valid opponent from the target pot.
        candidate_opponents = []
        for opponent_name, opponent_data in teams.items():
            if opponent_data["pot"] == target_pot:
                # Rule checks
                is_itself = opponent_name == team_name
                is_same_country = opponent_data["country"] == team_data["country"]
                is_already_opponent = opponent_name in team_data["opponents"]

                if is_itself or is_same_country or is_already_opponent:
                    continue

                # Check if the potential opponent also has a free slot for a team from our pot.
                opponent_opponents_from_our_pot = [
                    opp for opp in opponent_data["opponents"] if teams[opp]["pot"] == team_data["pot"]
                ]
                opponent_has_space = len(opponent_opponents_from_our_pot) < 2

                if opponent_has_space:
                    candidate_opponents.append(opponent_name)
        
        if not candidate_opponents:
            # If no valid opponent can be found at this stage, the entire draw attempt has failed.
            raise Exception(f"Draw deadlock: {team_name} could not find a valid opponent from pot {target_pot}.")

        # CORRECTED LOGIC: Be smarter about picking the best candidate to avoid deadlocks.
        def sort_key(opponent_name):
            """Calculates how "full" a potential opponent's schedule is from our perspective."""
            opp_data = teams[opponent_name]
            opponents_from_our_pot = [
                opp for opp in opp_data["opponents"] if teams[opp]["pot"] == team_data["pot"]
            ]
            return len(opponents_from_our_pot)

        # Sort all candidates by how "empty" they are.
        candidate_opponents.sort(key=sort_key)
        
        # Find the emptiness level of the best candidate(s).
        min_opponents_count = sort_key(candidate_opponents[0])
        
        # Create a list of all candidates that are equally "best".
        best_candidates = [
            opp for opp in candidate_opponents if sort_key(opp) == min_opponents_count
        ]
        
        # Randomly choose from this list of best options to break patterns.
        chosen_opponent = random.choice(best_candidates)
        
        teams[team_name]["opponents"].append(chosen_opponent)
        teams[chosen_opponent]["opponents"].append(team_name)

    # Final validation to ensure every team has exactly 8 opponents.
    for team_name, data in teams.items():
        if len(data["opponents"]) != 8:
            raise Exception(f"Validation failed: {team_name} has {len(data['opponents'])} opponents instead of 8.")

    return True

def print_draw_results(teams):
    """Formats and prints the final draw results in a clean way."""
    print("\n--- Custom Champions League League Phase Draw ---")
    
    sorted_teams = sorted(teams.keys(), key=lambda t: (teams[t]['pot'], t))
    
    for team_name in sorted_teams:
        team_data = teams[team_name]
        print(f"\n[{team_data['pot']}] {team_name} ({team_data['country']}) will play:")
        
        opponents_by_pot = collections.defaultdict(list)
        for opp in team_data["opponents"]:
            opp_pot = teams[opp]["pot"]
            opponents_by_pot[opp_pot].append(opp)
            
        for pot_num in sorted(opponents_by_pot.keys()):
            opp_list = ", ".join(sorted(opponents_by_pot[pot_num]))
            print(f"    Pot {pot_num}: {opp_list}")

# --- Main Program Execution ---
if __name__ == "__main__":
    print("Attempting to generate a valid UCL draw with custom rules...")
    
    max_attempts = 1000
    for attempt in range(1, max_attempts + 1):
        try:
            reset_draw(LEAGUE_TEAMS)
            if perform_draw(LEAGUE_TEAMS):
                print(f"\nSuccess! A valid draw was found on attempt #{attempt}.")
                print_draw_results(LEAGUE_TEAMS)
                break
        
        except Exception as e:
            if attempt == max_attempts:
                print(f"\nDraw failed after {max_attempts} attempts. Last error: {e}")
            else:
                # print(f"Attempt {attempt} failed. Retrying...") # Uncomment for verbose retries
                pass

