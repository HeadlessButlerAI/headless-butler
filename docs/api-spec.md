# API 接口规范 v1.0

本文档定义了 HeadlessButler AI 的标准 API 接口，AI Agent 可通过这些端点完成信息查询、时段检查、预订提交等操作。

---

## 基础信息

| 项目 | 值 |
|------|-----|
| 基础路径 | `/api` |
| 内容类型 | `application/json` |
| 字符编码 | UTF-8 |

---

## 端点列表

### 1. 服务发现 — `/welcome-ai`

AI 进入网站后的第一站，获取所有可用操作的能力清单。

- **方法**：`GET`
- **路径**：`/welcome-ai`
- **认证**：无

**响应示例**：

```json
{
  "service": "HeadlessButler AI",
  "version": "1.0.0",
  "description": "为网站提供 AI 可调用的标准 API 接口",
  "actions": [
    {
      "id": "get_info",
      "description": "获取商家基本信息",
      "method": "GET",
      "endpoint": "/api/info"
    },
    {
      "id": "check_availability",
      "description": "查询可预订时段",
      "method": "GET",
      "endpoint": "/api/availability",
      "parameters": {
        "date": "日期 (YYYY-MM-DD)",
        "party_size": "人数 (整数)"
      }
    },
    {
      "id": "make_reservation",
      "description": "提交预订",
      "method": "POST",
      "endpoint": "/api/reserve",
      "parameters": {
        "name": "客户姓名 (必填)",
        "phone": "联系电话 (必填)",
        "date": "日期 YYYY-MM-DD (必填)",
        "time": "时间 HH:MM (必填)",
        "party_size": "人数 (必填, 整数)",
        "notes": "特殊要求 (可选)"
      }
    }
  ]
}
```

---

### 2. 获取商家信息 — `GET /api/info`

返回商家的基本信息，供 AI 向用户展示。

- **方法**：`GET`
- **路径**：`/api/info`
- **认证**：无

**响应 200**：

```json
{
  "name": "月半湾西餐厅",
  "address": "示例路1号",
  "phone": "13800000000",
  "openingHours": "11:30-14:00, 17:30-21:00",
  "tablesAvailable": 5
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 商家名称 |
| address | string | 地址 |
| phone | string | 联系电话 |
| openingHours | string | 营业时间描述 |
| tablesAvailable | number | 当前可用桌数（可选） |

---

### 3. 查询可用时段 — `GET /api/availability`

查询指定日期和人数是否有可用时段。

- **方法**：`GET`
- **路径**：`/api/availability`
- **认证**：无

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 日期，格式 YYYY-MM-DD |
| party_size | number | 是 | 人数 |

**请求示例**：

```
GET /api/availability?date=2026-05-25&party_size=4
```

**响应 200**：

```json
{
  "date": "2026-05-25",
  "party_size": 4,
  "available": true,
  "slots": [
    { "time": "11:30", "available": true },
    { "time": "12:00", "available": true },
    { "time": "12:30", "available": false },
    { "time": "17:30", "available": true },
    { "time": "18:00", "available": true },
    { "time": "18:30", "available": true },
    { "time": "19:00", "available": true },
    { "time": "19:30", "available": false },
    { "time": "20:00", "available": true }
  ]
}
```

**响应 400**（参数错误）：

```json
{
  "error": "缺少必填参数",
  "detail": "请提供 date 和 party_size 参数"
}
```

---

### 4. 提交预订 — `POST /api/reserve`

AI 帮用户提交预订请求。

- **方法**：`POST`
- **路径**：`/api/reserve`
- **内容类型**：`application/json`
- **认证**：无

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 客户姓名 |
| phone | string | 是 | 联系电话 |
| date | string | 是 | 日期 YYYY-MM-DD |
| time | string | 是 | 时间 HH:MM |
| party_size | number | 是 | 人数 |
| notes | string | 否 | 特殊要求 |

**请求示例**：

```json
{
  "name": "张三",
  "phone": "13800000000",
  "date": "2026-05-25",
  "time": "19:00",
  "party_size": 4,
  "notes": "靠窗位置，有老人需要无障碍通道"
}
```

**响应 201**（创建成功）：

```json
{
  "success": true,
  "reservation_id": "R20260525-042",
  "message": "预订成功！2026年5月25日 19:00，4人桌。请提前5分钟到达。",
  "details": {
    "name": "张三",
    "date": "2026-05-25",
    "time": "19:00",
    "party_size": 4
  },
  "timestamp": "2026-05-23T12:00:00Z"
}
```

**响应 422**（数据校验失败）：

```json
{
  "error": "数据校验失败",
  "detail": "姓名不能为空"
}
```

---

## 错误码规范

| HTTP 状态码 | 含义 | 说明 |
|------------|------|------|
| 200 | OK | 请求成功（GET） |
| 201 | Created | 创建成功（POST） |
| 400 | Bad Request | 参数缺失或格式错误 |
| 404 | Not Found | 端点不存在 |
| 405 | Method Not Allowed | HTTP 方法不支持 |
| 422 | Unprocessable Entity | 请求体校验失败 |
| 429 | Too Many Requests | 请求频率超限 |
| 500 | Internal Server Error | 服务器内部错误 |

**错误响应格式**：

```json
{
  "error": "人类可读的错误摘要",
  "detail": "详细的错误说明"
}
```

---

## 速率限制

参考实现中，每个 IP 默认限制为 **每分钟 30 次请求**。生产环境建议根据实际情况调整，并加入 API Key 认证机制。

---

## Webhook 扩展

如果 API 需要对接现有业务系统（如 POS、CRM），可通过 Webhook 实现：

```json
// POST /api/reserve 内部流程
1. 接收并校验请求参数
2. 调用你的 Webhook URL（如 https://你的系统/webhook/reserve）
3. 将 Webhook 返回的结果返回给 AI
```

Webhook URL 通过环境变量 `WEBHOOK_RESERVE_URL` 配置。
