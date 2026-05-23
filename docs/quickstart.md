# 快速开始指南

本指南将帮助你在 5 分钟内为自己的网站接入 HeadlessButler AI 的"三层 VIP 通道"。

---

## 前置要求

- 一个网站（任何类型：静态 HTML、WordPress、自定义后端均可）
- 对网站根目录有文件写入权限

---

## 方式一：静态文件（零依赖，推荐入门）

适用于任何网站。只需在根目录添加两个文件：

### 第 1 步：添加 AI 邀请函

在网站根目录创建 `llms.txt`：

```markdown
# 你的网站名称
> 简短描述（一句话说清你的网站是什么）

## 核心能力
- 查看服务信息：GET /api/info
- 查询可用时段：GET /api/availability?date=YYYY-MM-DD
- 提交预订：POST /api/reserve

## 接口文档
完整规范请访问 /docs/api-spec.md
```

### 第 2 步：更新 robots.txt

确保 AI 爬虫有权访问你的网站：

```
User-agent: *
Allow: /

# 声明 AI 接口入口
# AI-Agent-Endpoint: https://你的域名.com/api
```

### 第 3 步：验证

用浏览器访问 `https://你的域名.com/llms.txt`，确认文件可正常访问。

---

## 方式二：运行参考服务器（完整功能）

如果你想提供完整的 AI API，选择一种语言的参考实现：

### Python (FastAPI)

```bash
cd server-python
pip install -r requirements.txt
python main.py
# 服务启动在 http://localhost:8000
```

### Node.js (Express)

```bash
cd server-node
npm install
node server.js
# 服务启动在 http://localhost:3000
```

---

## 方式三：部署到生产环境

### 无服务器函数

你可以将 API 端点部署为无服务器函数：

- **Vercel**：将 `api/` 目录导出为 Serverless Functions
- **Cloudflare Workers**：用 Workers 实现 API 路由
- **Netlify Functions**：在 `netlify/functions/` 下部署

### Docker

```bash
# Python 版本
docker build -t headless-butler-python ./server-python
docker run -p 8000:8000 headless-butler-python

# Node.js 版本
docker build -t headless-butler-node ./server-node
docker run -p 3000:3000 headless-butler-node
```

---

## 验证 AI 接入是否生效

### 1. 测试 /welcome-ai 端点

```bash
curl https://你的域名.com/welcome-ai
```

应返回结构化的 JSON 能力清单。

### 2. 测试 /api/info 端点

```bash
curl https://你的域名.com/api/info
```

应返回你的业务基本信息。

### 3. 测试预订接口

```bash
curl -X POST https://你的域名.com/api/reserve \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试用户",
    "phone": "13800000000",
    "date": "2026-05-25",
    "time": "19:00",
    "party_size": 4
  }'
```

---

## 下一步

- 阅读 [API 接口规范](./api-spec.md) 了解完整接口定义
- 查看 [项目概述](./overview.md) 了解设计理念
- 运行 [Demo 演示](../demo/index.html) 查看三层通道的交互效果

---

## 常见问题

### Q: 我的网站是 WordPress，怎么接入？

A: 最简单的方式是在根目录添加 `llms.txt` 文件。完整插件开发中。

### Q: HeadlessButler 会替换我的现有网站吗？

A: 不会。它是一层"附加接口"，你不改现有网站的任何代码，也不影响人类用户的访问体验。

### Q: 安全性怎么保证？

A: 参考实现包含速率限制和输入校验。生产环境建议加入 API Key 认证、HTTPS、CORS 白名单。
