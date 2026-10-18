import json
import time

ALLOWED_TYPES = {'enemy', 'hero', 'ally', 'boss', 'sub-boss', 'anti-hero', 'antagonist'}

# The high-level categories grouping your platforms and merchandise
SECTION_KEYS = {
    'consoles', 'handheld', 'hybrid', 'arcade', 
    'computer', 'mobile', 'games', 'toys', 'figurines'
}

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {file_path}.")
        return {}

def count_category_products(character_data):
    """
    Recursively sums game/item codes from arrays within the designated section groups.
    """
    total = 0
    for section in SECTION_KEYS:
        section_data = character_data.get(section)
        if isinstance(section_data, dict):
            for subcategory, items in section_data.items():
                if isinstance(items, list):
                    total += len(items)
    return total

def process_mario_data():
    start_time = time.perf_counter()

    # 1. Ingest Data
    combined_mario_data = {}
    combined_mario_data.update(load_json_file('enemies2.json'))
    combined_mario_data.update(load_json_file('characters2.json'))

    final_results = []

    # 2. Process Entries
    for character_key, character_data in combined_mario_data.items():
        if not isinstance(character_data, dict):
            continue

        char_type = str(character_data.get('type', 'Unknown')).lower()
        if char_type not in ALLOWED_TYPES:
            continue

        total_games = count_category_products(character_data)

        final_results.append({
            'name': character_data.get('name', character_key.capitalize()),
            'type': character_data.get('type', 'Unknown'),
            'debut': character_data.get('debut', 'Unknown'),
            'total_games': total_games
        })

    # 3. Sort Results (Descending)
    final_results.sort(key=lambda x: x['total_games'], reverse=True)

    # 4. Print Results
    print("\n--- Most to Least ---")
    for char in final_results[:1000]:
        print(f"{char['name']}: {char['total_games']} products total")

    total_time = time.perf_counter() - start_time
    print(f"\nTotal Time To Calculate: {total_time:.4f} seconds")
    print(f"Total entries aggregated: {len(final_results)}")

if __name__ == "__main__":
    process_mario_data()