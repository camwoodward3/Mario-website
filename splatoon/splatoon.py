import json
import time

ALLOWED_TYPES = {
    'protagonist', 'deuteragonist', 'antagonist', 'enemy', 'boss'
}
GAME_CATEGORIES = ('main', 'expansions', 'smash', 'mobile', 'crossovers')

def load_json_file(file_path):
  try:
    with open(file_path, 'r') as file:
      return json.load(file)
  except FileNotFoundError:
    print(f"Warning: {file_path} not found.")
    return {}
  except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {file_path}.")
    return {}

def process_splatoon_data():
  start_time = time.perf_counter()

  # 1. Read files directly in memory
  combined_splatoon_data = {}
  combined_splatoon_data.update(load_json_file('enemies.json'))
  combined_splatoon_data.update(load_json_file('splatoon.json'))

  final_results = []

  # 2. Process character items synchronously
  for character_key, character_data in combined_splatoon_data.items():
    if not isinstance(character_data, dict):
      continue

    # Normalize character types to lowercase list
    raw_type = character_data.get('type', 'Unknown')
    if isinstance(raw_type, list):
      char_types = [t.lower() for t in raw_type]
    else:
      char_types = [raw_type.lower()]

    # Efficient type checking using set intersection
    if not ALLOWED_TYPES.intersection(char_types):
      continue

    # Instant length summation without spawning threads or barriers
    total_games = sum(
      len(character_data.get(cat, [])) for cat in GAME_CATEGORIES
    )

    final_results.append({
      'name': character_data.get('name', character_key.capitalize()),
      'type': raw_type,
      'debut': character_data.get('debut', 'Unknown'),
      'copy': character_data.get('copy', 'Unknown'),
      'total_games': total_games
    })

  # 3. Sort leaderboard by total games
  final_results.sort(key=lambda x: x['total_games'], reverse=True)

  # 4. Print results
  print("\n--- Most to Least ---")
  for char in final_results:
    print(f"{char['name']} - {char['total_games']} games total")

  total_time = time.perf_counter() - start_time
  print(f"\nTotal Time to Calculate: {total_time:.4f} seconds")
  print(f"Total entries aggregated: {len(final_results)}")

if __name__ == "__main__":
  process_splatoon_data()