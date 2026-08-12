import json
import time

ALLOWED_TYPES = { 'player', 'special character', 'villager'}
GAME_CATEGORIES = (
  'main', 'expansions', 'spinoffs', 'software', 'smash', 'mobile', 'other'
)

def load_json_file(file_path):
  try:
    with open(file_path, 'r') as file:
      return json.load(file)
  except FileNotFoundError:
    print(f"Warning: {file_path} not found.")
    return {}
  except json.JSONDecodeError:
    print(f"Error decoding JSON in {file_path}.")
    return {}

def process_animal_data():
  start_time = time.perf_counter()

  combined_animal_data = {}

  combined_animal_data.update(load_json_file('special.json'))

  combined_animal_data.update(load_json_file('villager.json'))

  final_results = []

  for character_key, character_data in combined_animal_data.items():
    if not isinstance(character_data, dict):
      continue

    char_type = str(character_data.get('type', 'Unknown')).lower()
    if char_type not in ALLOWED_TYPES:
      continue

    total_games = sum(len(character_data.get(cat, [])) for cat in GAME_CATEGORIES)

    final_results.append({
      'name': character_data.get('name', character_key.capitalize()),
      'type': character_data.get('type', 'Unknown'),
      'debut': character_data.get('debut', 'Unknown'),
      'total_games': total_games
    })

    final_results.sort(key=lambda x: x['total_games'], reverse=True)

    print("\n--- Most to Least ---")
    for char in final_results:
      print(f"{char['name']} - {char['total_games']} games")

    total_time = time.perf_counter() - start_time
    print(f"\nTotal Time to Calculate: {total_time:.4f} seconds")
    print(f"Total categories aggregated: {len(final_results)}")

if __name__ == "__main__":
  process_animal_data()