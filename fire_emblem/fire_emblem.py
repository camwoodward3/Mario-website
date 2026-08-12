import json
import pydoc
import time

GAME_CATEGORIES = ('main', 'spinoffs', 'smash', 'other', 'crossovers')


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


def merge_character_data(combined, new_data):
  """Deep merges character data so entries across multiple JSON files

  combine their category lists rather than overwriting each other.
  """
  for char_key, char_info in new_data.items():
    if not isinstance(char_info, dict):
      continue

    # If the character isn't in combined yet, add them
    if char_key not in combined:
      combined[char_key] = char_info.copy()
    else:
      # If they already exist, merge metadata and category lists
      for key, value in char_info.items():
        if key in GAME_CATEGORIES and isinstance(value, list):
          # Combine game lists without duplicates
          existing_games = combined[char_key].get(key, [])
          combined[char_key][key] = list(set(existing_games).union(set(value)))
        elif key not in combined[char_key]:
          # Copy non-category properties if missing
          combined[char_key][key] = value


def process_emblem_data():
  start_time = time.perf_counter()

  combined_emblem_data = {}

  # Load and safely merge each JSON file
  json_files = ('playable.json', 'boss.json', 'allies.json', 'other.json')
  for file_name in json_files:
    data = load_json_file(file_name)
    merge_character_data(combined_emblem_data, data)

  final_results = []

  # Process character counts
  for character_key, character_data in combined_emblem_data.items():
    total_games = sum(
        len(character_data.get(cat, [])) for cat in GAME_CATEGORIES
    )

    final_results.append({
        'name': character_data.get('name', character_key.capitalize()),
        'class': character_data.get('class', 'Unknown'),
        'debut': character_data.get('debut', 'Unknown'),
        'total_games': total_games,
    })

  # Sort characters from most games to least games
  final_results.sort(key=lambda x: x['total_games'], reverse=True)

  # Format output lines
  output_lines = ["\n--- Most to Least ---"]
  for char in final_results:
    output_lines.append(f"{char['name']} - {char['total_games']} games")

  total_time = time.perf_counter() - start_time
  output_lines.append(f"\nTotal Time to Calculate: {total_time:.4f} seconds")
  output_lines.append(f"Total characters processed: {len(final_results)}")

  # Display via terminal pager so large outputs don't scroll past the buffer
  pydoc.pager("\n".join(output_lines))


if __name__ == "__main__":
  process_emblem_data()