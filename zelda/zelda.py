import json
import time

GAME_CATEGORIES = ('main', 'spinoff', 'smash', 'mobile', 'other')

def load_json_file(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error reading {file_path}: Invalid JSON.")
        return {}

def process_zelda_data():
    start_time = time.perf_counter()

    # 1. Read files directly in memory
    character_data = load_json_file("characters.json")
    enemy_data = load_json_file("enemies.json")

    # Combine both dictionaries instantly
    all_tasks = {**character_data, **enemy_data}
    final_results = []

    # 2. Process character items synchronously
    for character_key, item_data in all_tasks.items():
        if not isinstance(item_data, dict):
            continue

        # Calculate total games without sub-threading overhead
        total_games = sum(
            len(item_data.get(cat, [])) for cat in GAME_CATEGORIES
        )

        # Handle list vs string formatting cleanly
        raw_title = item_data.get("title", "Unknown")
        title_str = ", ".join(raw_title) if isinstance(raw_title, list) else str(raw_title)

        raw_species = item_data.get("species", "Unknown")
        species_str = ", ".join(raw_species) if isinstance(raw_species, list) else str(raw_species)

        final_results.append({
            'name': item_data.get('name', character_key.capitalize()),
            'species': species_str,
            'title': title_str,
            'debut': item_data.get('debut', 'Unknown'),
            'total_games': total_games
        })

    # 3. Sort leaderboard by total games
    final_results.sort(key=lambda x: x['total_games'], reverse=True)

    # 4. Print results
    print("\n--- Most to Least ---")
    for character in final_results:
        print(f"{character['name']} - {character['total_games']} games total")

    total_time = time.perf_counter() - start_time
    print(f"\nTotal Time To Calculate: {total_time:.4f} seconds")
    print(f"Total entries aggregated: {len(final_results)}")

if __name__ == "__main__":
    process_zelda_data()