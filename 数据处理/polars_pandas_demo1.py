# faker-25.0.0
# pip install pandas polars pytest psutil
#  pytest -s polars_pandas_demo1.py
from data_test_generate.data import *
import os

current_directory = os.path.dirname(__file__)
base_dir = os.path.dirname(current_directory)
import pandas as pd
import polars as pl
import time
import psutil
import os
import pytest

class ReadSpeedTest:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def generate_csv_data(self, max_num=100000):
        users = generate_users(max_num)
        write_to_csv(users, self.csv_file_path)
        print(f"CSV 文件已经生成，包含中文数据len{max_num}，并使用 UTF-8 编码。")
def measure_performance(library, file_path):
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    initial_cpu = process.cpu_times()
    start_time = time.time()

    if library == 'pandas':
        df = pd.read_csv(file_path)
    elif library == 'polars':
        df = pl.read_csv(file_path)

    total_time = time.time() - start_time
    memory_used = process.memory_info().rss - initial_memory
    end_cpu = process.cpu_times()
    cpu_time_used = (end_cpu.user - initial_cpu.user) + (end_cpu.system - initial_cpu.system)
    return total_time, memory_used, cpu_time_used

@pytest.fixture(scope="module")
def tester(tmp_path_factory):
    file_path = tmp_path_factory.mktemp("data") / "chinese_users.csv"
    test_obj = ReadSpeedTest(str(file_path))
    test_obj.generate_csv_data(100000)  # Generate 1000 records
    return test_obj

@pytest.mark.parametrize("library", ['pandas', 'polars'])
def test_csv_reading(tester, library):
    time_used, memory_used,cpu_time_used = measure_performance(library, tester.csv_file_path)
    print(f"{library} - Time: {time_used:.4f} seconds, Memory: {memory_used / 1024 / 1024:.2f} MB, CPU Time: {cpu_time_used:.4f} seconds")