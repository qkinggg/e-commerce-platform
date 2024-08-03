#!/bin/bash

# 註冊用戶
echo "註冊用戶..."
curl -X POST http://127.0.0.1:5000/auth/register -H "Content-Type: application/json" -d '{
    "email": "user@example.com",
    "password": "password"
}'

echo -e "\n\n"

# 登錄用戶並獲取訪問令牌
echo "登錄用戶..."
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "password"}' | jq -r '.access_token')

if [ "$TOKEN" == "null" ]; then
  echo "登錄失敗，無法獲取訪問令牌。"
  exit 1
fi

echo "獲取的訪問令牌：$TOKEN"
echo -e "\n\n"

# 訪問受保護的路由
echo "訪問受保護的路由..."
curl -X GET http://127.0.0.1:5000/auth/protected -H "Authorization: Bearer $TOKEN"
echo -e "\n\n"