import os
import numpy as np
import yaml
import shutil
from datetime import datetime
from async_life_game import AsyncLifeGame
from utils.csv_utils import save_csv

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    
    return config

def run_simulation(async_p, num_runs, size, max_t, num_states, probabilities):
    from_showing_graph = max_t

    results = []
    for _ in range(num_runs):
        game = AsyncLifeGame(size, num_states, probabilities, async_p)
        is_frozen, t = game._execute_plot(max_t, from_showing_graph)
        results.append([is_frozen, t])
    
    return results

def save_simulation_results(output_dir, async_p, num_runs, size, max_t, num_states, probabilities):
    filename = f"result_{async_p:.2f}.csv"
    filepath = os.path.join(output_dir, filename)

    results = run_simulation(async_p, num_runs, size, max_t, num_states, probabilities)
    print(results)

    save_csv(results, filepath)

def main():
    # 設定ファイルを読み込む
    config = load_config()
    
    # 日付付きフォルダの作成
    current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"{config['save_path']}_{current_date}"
    os.makedirs(output_dir, exist_ok=True)

    # 設定ファイルのコピー
    shutil.copy('config.yaml', os.path.join(output_dir, 'config.yaml'))

    num_runs = config['n']
    start = config['start']
    end = config['end']
    step = config['step']
    size = config['size']
    max_t = config['max_t']
    num_states = config['cnt_states']
    probabilities = config['probabilities']

    for async_p in np.arange(start, end + step, step):
        async_p = round(async_p, 2)
        print(f"In process: {async_p}")
        save_simulation_results(output_dir, async_p, num_runs, size, max_t, num_states, probabilities)

    print(f"All simulations are done. Results are saved in {output_dir}")

if __name__ == "__main__":
    main()
