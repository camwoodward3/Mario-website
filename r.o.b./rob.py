import json
import time

ALLOWED_TYPES = {'mechanical robot'}
GAME_CATEGORIES = ('games', 'smash', 'movies')

def process_rob_data(file_path='rob.json'):
  start_time = time.perf_counter()

  try:
    with open(file_path, 'r') as file:
      rob_data = json.load(file)
  except FileNotFoundError:
    print(f"Error: {file_path} not found.")
    return

  final_results = []

  for character_key, character_data in rob_data.items():
    if not isinstance(character_data, dict):
      continue

    raw_type = character_data.get('type', 'Unknown')
    if isinstance(raw_type, list):
      char_types = [t.lower() for t in raw_type]
    else:
      char_types = [raw_type.lower()]

    if not any(t in ALLOWED_TYPES for t in char_types):
      continue

    total_games = sum(len(character_data.get(cat, [])) for cat in GAME_CATEGORIES)

    final_results.append({
      'name': character_data.get('name', character_key.capitalize()),
      'type': raw_type,
      'debut': character_data.get('debut', 'Unknown'),
      'total_games': total_games
    })

    final_results.sort(key=lambda x: x['total_games'], reverse=True)

    print("\n--- Most to Least ---")
    for char in final_results:
      print(f"{char['name']} - {char['total_games']} games total")

    total_time = time.perf_counter() - start_time
    print(f"\nTotal Time to Calculate: {total_time:.4f} seconds")
    print(f"Total entries aggregated: {len(final_results)}")

if __name__ == "__main__":
  process_rob_data()