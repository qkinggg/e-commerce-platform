#!/bin/bash

# 添加產品
echo "添加產品..."
ADD_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/product/add -H "Content-Type: application/json" -d '{
    "name": "Sample Product",
    "description": "This is a sample product",
    "price": 19.99,
    "stock": 100,
    "image_url": "http://example.com/image.jpg"
}')

PRODUCT_ID=$(echo $ADD_RESPONSE | jq -r '.id')

if [ "$PRODUCT_ID" == "null" ]; then
  echo "產品添加失敗，無法獲取產品ID。"
  exit 1
fi

echo "產品添加成功，ID：$PRODUCT_ID"
echo -e "\n\n"

# 查看產品
echo "查看產品..."
GET_RESPONSE=$(curl -s -X GET http://127.0.0.1:5000/product/$PRODUCT_ID)

echo $GET_RESPONSE | jq
echo -e "\n\n"

# 更新產品
echo "更新產品..."
curl -s -X PUT http://127.0.0.1:5000/product/$PRODUCT_ID -H "Content-Type: application/json" -d '{
    "price": 29.99,
    "stock": 50
}' | jq

echo "產品更新成功"
echo -e "\n\n"
<<EOF
# 刪除產品
echo "刪除產品..."
curl -s -X DELETE http://127.0.0.1:5000/product/$PRODUCT_ID | jq

echo "產品刪除成功"
echo -e "\n\n"
EOF
# 上傳圖片
echo "上傳圖片..."
curl -s -X POST http://127.0.0.1:5000/product/upload_image -F "image=@./pic/sample.png" | jq

echo "圖片上傳成功"
echo -e "\n\n"
