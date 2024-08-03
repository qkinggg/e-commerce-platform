# keep_alive.py
# Keep MongoDB Atlas cluster alive to avoid automatic pausing

from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

# 加載 .env 文件中的環境變量
load_dotenv()

# 從環境變量中獲取 MongoDB 密碼
password = os.getenv('MONGO_PASSWORD')

# 設置 MongoDB 連接字符串，替換 <password> 為實際密碼
uri = f"mongodb+srv://root:{password}@mycluster.qarbhqo.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"

# 創建一個新的客戶端並連接到服務器
client = MongoClient(uri)

# 發送 ping 命令以確認連接成功
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)