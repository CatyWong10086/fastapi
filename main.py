from fastapi import FastAPI, HTTPException
import pandas as pd
import os
import logging
import random

# 初始化 FastAPI 应用
app = FastAPI()

# 在应用启动时检查 'data.csv' 和 'cache.csv' 文件是否存在，如果不存在则创建空的 CSV 文件
if not os.path.exists('data.csv'):
    pd.DataFrame({'ID': [], 'q': [], 'a': []}).to_csv('data.csv', index=False)
if not os.path.exists('cache.csv'):
    pd.DataFrame({'ID': [], 'q': [], 'a': []}).to_csv('cache.csv', index=False)

# 配置日志，设置日志级别为 DEBUG
logging.basicConfig(level=logging.DEBUG)

# 在应用启动时执行的事件
@app.on_event("startup")
async def startup_event():
    print("应用启动完成，正在检查数据文件。")
    if not os.path.exists('data.csv'):
        print("未找到 data.csv 文件。")
    else:
        print("已找到 data.csv 文件，正在检查内容...")
        data_df = pd.read_csv('data.csv')
        if data_df.empty:
            print("data.csv 文件为空。")
        else:
            print(f"data.csv 包含 {len(data_df)} 行数据。")

# 定义一个 GET 请求的端点，用于从 'data.csv' 中随机检索一条数据
@app.get("/")
async def random_retrieve():
    print("正在访问 /random_retrieve 端点。")
    data_df = pd.read_csv('data.csv')
    if data_df.empty:
        print("data.csv 中没有可用数据。")
        raise HTTPException(status_code=404, detail="No data available")

    random_row = data_df.sample(n=1)
    random_data = random_row.iloc[0]
    print(f"随机检索到的数据: {random_data.to_dict()}")

    # 将随机检索到的数据写入到 cache.csv
    cache_df = pd.DataFrame([random_data])  # 创建一个包含随机数据的 DataFrame
    cache_df.to_csv('cache.csv', index=False)  # 写入到 cache.csv 文件中，没有索引

    # 打印日志确认数据
    print("缓存数据已写入:", random_data.to_dict())
    return [random_data.to_dict()]

# 定义一个 GET 请求的端点，用于从 'cache.csv' 中检索数据
@app.get("/retrieve_from_cache")
async def retrieve_from_cache():
    cache_df = pd.read_csv('cache.csv')
    if cache_df.empty:
        raise HTTPException(status_code=404, detail="缓存为空")


    cached_data = cache_df.iloc[0]

    return [{"ID": cached_data['ID'], "q": cached_data['Q'], "a": cached_data['A'], "Source": "Cache"}]
