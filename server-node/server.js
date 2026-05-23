/**
 * HeadlessButler AI — Node.js (Express) 参考实现
 * ===============================================
 * 三层 VIP 通道的完整 API 服务端实现。
 *
 * 启动方式：
 *     npm install
 *     node server.js
 *     访问 http://localhost:3000
 */

const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(express.json());
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "*");
    res.header("Access-Control-Allow-Methods", "*");
    next();
});

// ============================================================
// 模拟数据
// ============================================================

const MOCK_INFO = {
    name: "月半湾西餐厅 (Demo)",
    address: "示例路1号",
    phone: "13800000000",
    openingHours: "11:30-14:00, 17:30-21:00",
    tablesAvailable: 5,
};

const MOCK_SLOTS = [
    { time: "11:30", available: true },
    { time: "12:00", available: true },
    { time: "12:30", available: false },
    { time: "17:30", available: true },
    { time: "18:00", available: true },
    { time: "18:30", available: true },
    { time: "19:00", available: true },
    { time: "19:30", available: false },
    { time: "20:00", available: true },
];

function validateReservation(body) {
    const errors = [];
    if (!body.name || body.name.trim() === "") errors.push("姓名不能为空");
    if (!body.phone || body.phone.trim() === "") errors.push("电话不能为空");
    if (!body.date) errors.push("日期不能为空");
    if (!body.time) errors.push("时间不能为空");
    if (!body.party_size || body.party_size < 1) errors.push("人数必须大于0");
    return errors;
}

// ============================================================
// 第一层：服务发现 /welcome-ai
// ============================================================

app.get("/welcome-ai", (req, res) => {
    res.json({
        service: "HeadlessButler AI",
        version: "1.0.0",
        description: "为网站提供 AI 可调用的标准 API 接口",
        actions: [
            {
                id: "get_info",
                description: "获取商家基本信息（名称、地址、营业时间）",
                method: "GET",
                endpoint: "/api/info",
            },
            {
                id: "check_availability",
                description: "查询可预订时段",
                method: "GET",
                endpoint: "/api/availability",
                parameters: {
                    date: "日期 (YYYY-MM-DD)",
                    party_size: "人数 (整数)",
                },
            },
            {
                id: "make_reservation",
                description: "提交预订",
                method: "POST",
                endpoint: "/api/reserve",
                parameters: {
                    name: "客户姓名 (必填)",
                    phone: "联系电话 (必填)",
                    date: "日期 YYYY-MM-DD (必填)",
                    time: "时间 HH:MM (必填)",
                    party_size: "人数 (必填)",
                    notes: "特殊要求 (可选)",
                },
            },
        ],
    });
});

// ============================================================
// 第三层：业务 API 端点
// ============================================================

app.get("/api/info", (req, res) => {
    res.json(MOCK_INFO);
});

app.get("/api/availability", (req, res) => {
    const { date, party_size } = req.query;
    if (!date || !party_size) {
        return res.status(400).json({
            error: "缺少必填参数",
            detail: "请提供 date 和 party_size 参数",
        });
    }
    const hasAny = MOCK_SLOTS.some(s => s.available);
    res.json({
        date,
        party_size: parseInt(party_size),
        available: hasAny,
        slots: MOCK_SLOTS,
    });
});

app.post("/api/reserve", (req, res) => {
    const errors = validateReservation(req.body);
    if (errors.length > 0) {
        return res.status(422).json({
            error: "数据校验失败",
            detail: errors[0],
        });
    }

    const { name, phone, date, time, party_size, notes } = req.body;
    const datePart = date.replace(/-/g, "");
    const seq = String(Math.floor(Math.random() * 900) + 100);
    const reservationId = `R${datePart}-${seq}`;

    res.status(201).json({
        success: true,
        reservation_id: reservationId,
        message: `预订成功！${date} ${time}，${party_size}人桌。请提前5分钟到达。`,
        details: { name, date, time, party_size },
        timestamp: new Date().toISOString(),
    });
});

// ============================================================
// 启动
// ============================================================

app.listen(PORT, () => {
    console.log(`🤖 HeadlessButler AI 服务器已启动`);
    console.log(`📨 服务单: http://localhost:${PORT}/welcome-ai`);
    console.log(`📡 商家信息: http://localhost:${PORT}/api/info`);
    console.log(`📅 时段查询: http://localhost:${PORT}/api/availability?date=2026-05-25&party_size=4`);
    console.log(`📝 预订接口: POST http://localhost:${PORT}/api/reserve`);
});
