#!/bin/bash

echo "登錄admin..."
ADMIN_TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d '{"email": "admin@example.com", "password": "admin"}' | jq -r '.access_token')
echo $ADMIN_TOKEN

# 查看所有產品
echo "查看所有產品..."
curl -s -X GET http://127.0.0.1:5000/admin/products -H "Authorization: Bearer $ADMIN_TOKEN" | jq
echo -e "\n\n"

# 查看所有訂單
echo "查看所有訂單..."
curl -s -X GET http://127.0.0.1:5000/admin/orders -H "Authorization: Bearer $ADMIN_TOKEN" | jq
echo -e "\n\n"

# 刪除產品
echo "刪除產品..."
PRODUCT_ID=$(curl -s -X GET http://127.0.0.1:5000/admin/products -H "Authorization: Bearer $ADMIN_TOKEN" | jq -r '.[-1]._id')
echo $PRODUCT_ID
curl -s -X DELETE http://127.0.0.1:5000/admin/product/$PRODUCT_ID -H "Authorization: Bearer $ADMIN_TOKEN" | jq
echo -e "\n\n"

# 更新訂單狀態
echo "更新訂單狀態..."
ORDER_ID=$(curl -s -X GET http://127.0.0.1:5000/admin/orders -H "Authorization: Bearer $ADMIN_TOKEN" | jq -r '.[-1]._id')
NEW_STATUS="shipped"  # 可以根據需要更改為其他狀態，如 'canceled'

curl -s -X PUT http://127.0.0.1:5000/admin/order/$ORDER_ID -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{
    "status": "'"$NEW_STATUS"'"
}' | jq
echo -e "\n\n"
