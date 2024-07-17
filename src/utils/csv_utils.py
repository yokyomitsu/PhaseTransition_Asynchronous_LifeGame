import csv

def save_csv(data, filename):
    """CSVファイルに書き込む"""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

    print(f"{filename} に保存されました。")
    return True

def load_csv(filename):
    """CSVファイルから読み込む"""
    data = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    print(f"{filename} から読み込みました。")
    return data

def main():
    filename = 'ca_async_result/result_0.01.csv'
    data = load_csv(filename)
    print(data)

if __name__ == "__main__":
    main()
