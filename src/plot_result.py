import matplotlib.pyplot as plt
from utils.csv_utils import load_csv
import numpy as np
import yaml
import os

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def aggregate_results(data_folder, config):
    start = config['start']
    end = config['end']
    step = config['step']
    num_runs = config['n']

    x_values = []
    y_values = []

    for async_p in np.arange(start, end + step, step):
        async_p = round(async_p, 2)  # ファイル名統一
        filename = f'{data_folder}/result_{async_p:.2f}.csv'
        data = np.array(load_csv(filename))
        cnt_frozen = sum(1 for item in data if item[0] == 'True')
        frozen_rate = round(cnt_frozen / num_runs, 2)
        print(f"async_p:{async_p}, {frozen_rate}")

        # グラフ表示用に保持
        x_values.append(async_p)
        y_values.append(frozen_rate)
    
    return x_values, y_values

def save_graph(x_values, y_values, output_dir):
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    plt.title('Phase Transition of Asynchronous Life Game')
    plt.xlabel('Asynchronous Update Probability')
    plt.ylabel('Frozen Rate')
    plt.grid(True)

    # x軸の範囲とラベルを設定
    x_ticks = x_values
    x_labels = [f"{tick:.2f}" for tick in x_ticks]
    plt.xticks(ticks=x_ticks, labels=x_labels)

    graph_filename = os.path.join(output_dir, 'frozen_rate_graph.png')
    plt.savefig(graph_filename)
    plt.close()

def main():
    data_folder = 'result_20240717_141959'  # ここに指定されたデータフォルダの名前を入れる
    config = load_config()

    x_values, y_values = aggregate_results(data_folder, config)

    save_graph(x_values, y_values, data_folder)

    print(f"Graph saved in {data_folder}")

if __name__ == "__main__":
    main()
