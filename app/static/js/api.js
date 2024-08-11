// app/static/js/api.js

// 獲取 JWT token
function getToken() {
    return localStorage.getItem('access_token');
}

// 通用的 API 請求方法
async function apiRequest(endpoint, method = 'GET', body = null) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json'
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(endpoint, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
    });

    return response.json();
}

// 示例：獲取產品列表
async function getProducts() {
    const data = await apiRequest('/product/list');
    return data;
}

// 示例：登錄
async function login(email, password) {
    const data = await apiRequest('/auth/login', 'POST', { email, password });
    if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
    }
    return data;
}
