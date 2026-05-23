# 🤖 HeadlessButler AI

**为你的网站开通 AI 专用 VIP 通道。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Early Stage](https://img.shields.io/badge/Status-Early%20Stage-orange)](https://github.com/HeadlessButlerAI/headless-butler)

---

## 💡 这是什么？

HeadlessButler AI 是一个**开源的无头网站 AI 管家框架**。

它让任何 AI Agent（ChatGPT、Claude、Kimi 等）都能像人类一样读懂、使用你的网站——查询信息、预订服务、下单交易，全自动完成。

> ⚠️ 我们不是另一个 AI 聊天机器人。  
> ✅ 我们是你网站背后，专门服务 AI 的"接待层"。

---

## 🎯 三层 VIP 通道
📨 第一层：邀请函 (llms.txt) → AI 搜索发现你
📋 第二层：服务单 (/welcome-ai) → AI 了解你能做什么
⚡ 第三层：包间 (API 端点) → AI 直接完成操作
| 层级 | 作用 | 实现 |
|------|------|------|
| 邀请函 | 让 AI 搜索引擎优先推荐你的网站 | `llms.txt` + `robots.txt` |
| 服务单 | 用结构化 JSON 列出所有可用操作 | `/welcome-ai` 端点 |
| 包间 | 查询、预订、下单全通过 API 调用 | RESTful API 端点 |

---

## 🚧 项目状态

🚀 **早期构建阶段**，正在开发第一个可用原型。

- [x] 项目定位与架构设计
- [x] llms.txt 标准定义
- [x] Demo 演示页面
- [ ] API 规范文档
- [ ] 参考实现（Node.js）
- [ ] WordPress 插件

欢迎 ⭐ Star 关注进展，也欢迎通过 Issue 讨论任何关于"AI 如何与网站交互"的想法。

---

## 📂 项目结构
headless-butler/
├── README.md # 项目概述
├── llms.txt # AI 专用服务指南
├── robots.txt # 爬虫规则
├── sitemap.xml # 站点地图
├── LICENSE # MIT 许可证
├── demo/
│ └── index.html # 三层 VIP 通道演示
├── docs/
│ ├── overview.md # 项目概述文档
│ ├── quickstart.md # 快速开始指南
│ └── api-spec.md # API 接口规范
└── specs/
└── welcome-ai.json # /welcome-ai 数据结构定义
---

## 🔧 快速开始

### 第一步：添加 AI 邀请函

在你的网站根目录添加 `llms.txt`：

```markdown
# 你的网站名
> 简短描述

## 核心能力
- 查看服务：GET /api/info
- 提交预订：POST /api/reserve


##🤝 适用场景
🍽️ 餐厅在线订位
🏨 酒店房间查询与预订
🛍️ 零售门店库存查询
🏢 企业官网服务预约
📅 诊所/美容院预约挂号
🎫 任何需要 AI Agent 直接操作的网站
