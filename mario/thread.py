import json
import time

ALLOWED_TYPES = {'enemy', 'hero', 'ally', 'boss', 'sub-boss', 'anti-hero', 'antagonist'}
GAME_CATEGORIES = (
    'main', 'kart', 'smash', 'party', 'sports', 
    'rpg', 'shows', 'movies', 'arcade', 'gamewatch', 'mobile', 'other', 'crossovers'
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

def process_mario_data():
  start_time = time.perf_counter()

  # 1. Direct Data Ingestion (In Memory)
  combined_mario_data = {}
  combined_mario_data.update(load_json_file('enemies.json'))
  combined_mario_data.update(load_json_file('characters.json'))

  final_results = []

  # 2. Process Data Directly
  for character_key, character_data in combined_mario_data.items():
    if not isinstance(character_data, dict):
      continue

    # Type Filtering
    char_type = str(character_data.get('type', 'Unknown')).lower()
    if char_type not in ALLOWED_TYPES:
      continue

    # Sum up category occurrences instantly without threads or barriers
    total_games = sum(
      len(character_data.get(cat, [])) for cat in GAME_CATEGORIES
    )

    final_results.append({
      'name': character_data.get('name', character_key.capitalize()),
      'type': character_data.get('type', 'Unknown'),
      'debut': character_data.get('debut', 'Unknown'),
      'total_games': total_games
    })

  # 3. Sort Results
  final_results.sort(key=lambda x: x['total_games'], reverse=True)

  # 4. Print Results
  print("\n--- Most to Least ---")
  for char in final_results:
    print(f"{char['name']} - {char['total_games']} games total")

  total_time = time.perf_counter() - start_time
  print(f"\nTotal Time To Calculate: {total_time:.4f} seconds")
  print(f"Total entries aggregated: {len(final_results)}")

if __name__ == "__main__":
  process_mario_data()