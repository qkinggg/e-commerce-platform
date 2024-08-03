#!/bin/bash

echo "登錄用戶..."
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "password"}' | jq -r '.access_token')



# 獲取所有產品並提取第一個和第二個產品的ID
PRODUCT_IDS=$(curl -s -X GET http://127.0.0.1:5000/product/list | jq -r '.[0,1]._id')
PRODUCT_ID_ARRAY=($(echo $PRODUCT_IDS | tr -d '\r'))

# 提取第一個和第二個產品的ID到變量
PRODUCT_ID_1=${PRODUCT_ID_ARRAY[0]}
PRODUCT_ID_2=${PRODUCT_ID_ARRAY[1]}

if [ -z "$PRODUCT_ID_1" ] || [ -z "$PRODUCT_ID_2" ]; then
  echo "無法獲取產品ID。請確保有足夠的可用產品。"
  exit 1
fi

echo "使用的第一個產品ID：$PRODUCT_ID_1"
echo "使用的第二個產品ID：$PRODUCT_ID_2"
echo -e "\n\n"

# 添加第一個產品到購物車
echo "添加第一個產品到購物車..."
curl -s -X POST http://127.0.0.1:5000/cart/add -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{
    \"product_id\": \"$PRODUCT_ID_1\",
    \"quantity\": 3
}" | jq

echo -e "\n\n"

# 查看購物車
echo "查看購物車..."
curl -s -X GET http://127.0.0.1:5000/cart/view -H "Authorization: Bearer $TOKEN" | jq
echo -e "\n\n"

# 移除產品從購物車
echo "移除產品從購物車..."
curl -s -X POST http://127.0.0.1:5000/cart/remove -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{
    \"product_id\": \"$PRODUCT_ID_1\"
}" | jq

echo -e "\n\n"

# 添加第一個產品到購物車
echo "添加第一個產品到購物車..."
curl -s -X POST http://127.0.0.1:5000/cart/add -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{
    \"product_id\": \"$PRODUCT_ID_1\",
    \"quantity\": 3
}" | jq

echo -e "\n\n"

# 添加第二個產品到購物車
echo "添加第二個產品到購物車..."
curl -s -X POST http://127.0.0.1:5000/cart/add -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{
    \"product_id\": \"$PRODUCT_ID_2\",
    \"quantity\": 1
}" | jq

echo -e "\n\n"
