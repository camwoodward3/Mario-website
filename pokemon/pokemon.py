import json
import time

GAME_CATEGORIES = (
    'main', 'side', 'stadium', 'snap', 'spinoffs', 'other', 'trading', 'smash', 'rpg', 'arcade', 'mini', 'pc', 'mobile', 'others', 'crossovers', 'advanced', 'movies', 'anime'
)

def process_pokemon_data(file_path='pokemon.json', output_path='pokemon_game_counts.txt'):
  start_time = time.perf_counter()

  # 1. Direct Data Ingestion
  try:
    with open(file_path, 'r', encoding='utf-8') as file:
      raw_data = json.load(file)
  except FileNotFoundError:
    print(f"Error: {file_path} not found.")
    return
  except json.JSONDecodeError:
    print(f"Error reading {file_path}: Invalid JSON.")
    return

  combined_pokemon_data = {}
  for gen_key, gen_data in raw_data.items():
    if isinstance(gen_data, dict):
      combined_pokemon_data.update(gen_data)

  final_results = []

  # 2. Process Data Synchronously
  for pokemon_key, pokemon_data in combined_pokemon_data.items():
    if not isinstance(pokemon_data, dict):
      continue

    # Normalize types to a list
    poke_types = pokemon_data.get('type', [])
    if isinstance(poke_types, str):
      poke_types = [poke_types]

    # Calculate total game appearances inline
    total_games = sum(
      len(pokemon_data.get(cat, [])) for cat in GAME_CATEGORIES
    )

    final_results.append({
      'name': pokemon_data.get('name', pokemon_key.capitalize()),
      'types': poke_types,
      'debut': pokemon_data.get('debut', 'Unknown'),
      'species': pokemon_data.get('species', 'Unknown'),
      'total_games': total_games
    })

  # 3. Sort Results
  final_results.sort(key=lambda x: x['total_games'], reverse=True)

  # 4. Write Results to File & Print Summary to Terminal
  total_time = time.perf_counter() - start_time

  with open(output_path, 'w', encoding='utf-8') as out_file:
    out_file.write("--- Most to Least Appearances ---\n")
    for poke in final_results:
      types_str = "/".join(poke['types'])
      out_file.write(f"{poke['name']} - {poke['total_games']} games total\n")

    out_file.write(f"\nTotal Time to Calculate: {total_time:.4f} seconds\n")
    out_file.write(f"Total entries aggregated: {len(final_results)}\n")

  # Terminal Output (Summary + Preview of Top 10)
  print(f"Success! Processed {len(final_results)} entries in {total_time:.4f} seconds.")
  print(f"Full results saved to: {output_path}\n")
  print("--- Top 10 Preview ---")
  for poke in final_results[:700]:
    print(f"{poke['name']} - {poke['total_games']} games total")

if __name__ == "__main__":
  process_pokemon_data()