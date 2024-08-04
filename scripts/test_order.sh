#!/bin/bash

echo "登錄admin..."
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d '{"email": "admin@example.com", "password": "admin"}' | jq -r '.access_token')

# 創建訂單
echo "創建訂單..."
CREATE_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/order/create -H "Authorization: Bearer $TOKEN")
echo "Create Response: $CREATE_RESPONSE"

ORDER_ID=$(echo $CREATE_RESPONSE | jq -r '.order_id')

if [ "$ORDER_ID" == "null" ]; then
  echo "訂單創建失敗。"
  exit 1
fi

echo "訂單創建成功，ID：$ORDER_ID"
echo -e "\n\n"
sleep 3
# 查看訂單
echo "查看訂單..."
curl -s -X GET http://127.0.0.1:5000/order/$ORDER_ID -H "Authorization: Bearer $TOKEN" | jq
echo -e "\n\n"

# 支付訂單
echo "支付訂單..."
curl -s -X POST http://127.0.0.1:5000/order/pay -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{
    "order_id": "'"$ORDER_ID"'"
}' | jq

echo "訂單支付成功"
echo -e "\n\n"
