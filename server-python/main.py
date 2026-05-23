"""
HeadlessButler AI — Python (FastAPI) 参考实现
=============================================
三层 VIP 通道的完整 API 服务端实现。

启动方式：
    pip install -r requirements.txt
    python main.py
    访问 http://localhost:8000/docs 查看 Swagger UI
"""

from datetime import datetime, date, time
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import random

app = FastAPI(
    title="HeadlessButler AI",
    description="为你的网站开通 AI 专用 VIP 通道",
    version="1.0.0",
)

# CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 数据模型
# ============================================================

class ReservationRequest(BaseModel):
    """预订请求体"""
    name: str = Field(..., description="客户姓名", min_length=1, max_length=50)
    phone: str = Field(..., description="联系电话", min_length=5, max_length=20)
    date: str = Field(..., description="日期 YYYY-MM-DD", pattern=r"^\d{4}-\d{2}-\d{2}$")
    time: str = Field(..., description="时间 HH:MM", pattern=r"^\d{2}:\d{2}$")
    party_size: int = Field(..., description="人数", ge=1, le=20)
    notes: str = Field(default="", description="特殊要求", max_length=500)


class InfoResponse(BaseModel):
    name: str
    address: str
    phone: str
    openingHours: str
    tablesAvailable: int


class SlotInfo(BaseModel):
    time: str
    available: bool


class AvailabilityResponse(BaseModel):
    date: str
    party_size: int
    available: bool
    slots: list[SlotInfo]


class ReservationDetail(BaseModel):
    name: str
    date: str
    time: str
    party_size: int


class ReservationResponse(BaseModel):
    success: bool
    reservation_id: str
    message: str
    details: ReservationDetail
    timestamp: str


class WelcomeAction(BaseModel):
    id: str
    description: str
    method: str
    endpoint: str
    parameters: Optional[dict] = None


class WelcomeResponse(BaseModel):
    service: str
    version: str
    description: str
    actions: list[WelcomeAction]


# ============================================================
# 模拟数据
# ============================================================

MOCK_SLOTS = [
    {"time": "11:30", "available": True},
    {"time": "12:00", "available": True},
    {"time": "12:30", "available": False},
    {"time": "17:30", "available": True},
    {"time": "18:00", "available": True},
    {"time": "18:30", "available": True},
    {"time": "19:00", "available": True},
    {"time": "19:30", "available": False},
    {"time": "20:00", "available": True},
]

MOCK_INFO = {
    "name": "月半湾西餐厅 (Demo)",
    "address": "示例路1号",
    "phone": "13800000000",
    "openingHours": "11:30-14:00, 17:30-21:00",
    "tablesAvailable": 5,
}


# ============================================================
# 第一层入口：服务发现 /welcome-ai
# ============================================================

@app.get("/welcome-ai", response_model=WelcomeResponse, tags=["VIP 通道"])
async def welcome_ai():
    """AI 进入网站后收到的结构化能力清单"""
    return {
        "service": "HeadlessButler AI",
        "version": "1.0.0",
        "description": "为网站提供 AI 可调用的标准 API 接口",
        "actions": [
            {
                "id": "get_info",
                "description": "获取商家基本信息（名称、地址、营业时间）",
                "method": "GET",
                "endpoint": "/api/info",
            },
            {
                "id": "check_availability",
                "description": "查询可预订时段",
                "method": "GET",
                "endpoint": "/api/availability",
                "parameters": {
                    "date": "日期 (YYYY-MM-DD)",
                    "party_size": "人数 (整数)",
                },
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
                    "party_size": "人数 (必填)",
                    "notes": "特殊要求 (可选)",
                },
            },
        ],
    }


# ============================================================
# 第三层：业务 API 端点
# ============================================================

@app.get("/api/info", response_model=InfoResponse, tags=["业务 API"])
async def get_info():
    """获取商家基本信息"""
    return MOCK_INFO  # type: ignore[return-value]


@app.get("/api/availability", response_model=AvailabilityResponse, tags=["业务 API"])
async def get_availability(
    date: str = Query(..., description="日期 YYYY-MM-DD", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    party_size: int = Query(..., description="人数", ge=1, le=20),
):
    """查询指定日期的可用时段"""
    has_any = any(s["available"] for s in MOCK_SLOTS)
    return {
        "date": date,
        "party_size": party_size,
        "available": has_any,
        "slots": MOCK_SLOTS,
    }


@app.post("/api/reserve", status_code=201, response_model=ReservationResponse, tags=["业务 API"])
async def make_reservation(req: ReservationRequest):
    """提交预订请求"""
    # 生成预订 ID
    date_part = req.date.replace("-", "")
    seq = random.randint(1, 999)
    reservation_id = f"R{date_part}-{seq:03d}"

    return {
        "success": True,
        "reservation_id": reservation_id,
        "message": f"预订成功！{req.date} {req.time}，{req.party_size}人桌。请提前5分钟到达。",
        "details": {
            "name": req.name,
            "date": req.date,
            "time": req.time,
            "party_size": req.party_size,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


# ============================================================
# 启动
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
