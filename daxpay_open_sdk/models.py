"""请求/响应模型 — 对照 sdk-contract.md 第四、五、6.1 节

键名即报文键名（camelCase），SDK 直接序列化该 dict，不做键名转换。
TypedDict 仅用于编辑器提示，运行时就是普通 dict；标注「必填」的键必须由调用方提供。
"""
from __future__ import annotations

from typing import Any, List, Optional, TypedDict


class DaxResult(TypedDict, total=False):
    """统一响应结构（契约第五节）"""

    code: int  # 业务状态码，0 成功，非 0 失败
    msg: str  # 提示信息（是 msg 非 message）
    data: Optional[Any]  # 业务数据，失败时通常 null
    sign: str  # 平台 RSA 响应签名（Base64）
    resTime: str  # 响应时间（北京时间 yyyy-MM-dd HH:mm:ss）
    reqId: str  # 请求 ID 回显


class CommonParam(TypedDict, total=False):
    """公共请求参数（所有业务请求继承，对照契约第四节）"""

    mchNo: str
    appId: str
    reqId: str
    reqTime: str  # 请求时间（SDK 自动生成，北京时间 yyyy-MM-dd HH:mm:ss 字面量）
    nonceStr: str
    clientIp: str
    sign: str


class TerminalInfo(TypedDict, total=False):
    """终端信息（线下场景）"""

    terminalNo: str
    storeNo: str
    operatorId: str
    deviceName: str
    deviceIp: str
    longitude: float
    latitude: float


class GoodsDetail(TypedDict, total=False):
    """商品明细"""

    goodsId: str  # 必填
    goodsName: str  # 必填
    quantity: int  # 必填
    unitPrice: int  # 必填，单位：分
    category: str
    description: str
    showUrl: str


class PayParam(CommonParam, total=False):
    """支付下单请求参数（契约 6.1 节）"""

    bizOrderNo: str  # 必填，商户订单号
    title: str  # 必填，支付标题
    description: str
    amount: int  # 必填，支付金额（分）
    currency: str  # 币种 ISO 4217，缺省 cny
    product: str  # 支付产品编码（空则路由自动选择）
    method: str  # 支付方式编码
    capability: str
    openId: str
    channelAppId: str
    authCode: str
    limitPay: List[str]  # 限制支付类型，如 ["no_credit"]
    extraParam: str  # 支付扩展参数（JSON 字符串）
    goodsDetail: List[GoodsDetail]
    notifyUrl: str  # 异步通知地址
    returnUrl: str  # 同步跳转地址
    attach: str  # 商户扩展参数，回调原样返回
    expiredTime: str  # 过期时间（北京时间 yyyy-MM-dd HH:mm:ss，空默认 30 分钟）
    terminal: TerminalInfo


class PayResult(TypedDict, total=False):
    """支付下单响应结果（契约 6.1 节）"""

    orderId: int
    bizOrderNo: str  # 商户订单号
    orderNo: str  # 平台业务单号
    tradeNo: str  # 资金交易号
    status: str  # wait / progress / success / close / cancel / fail / timeout
    payBody: str  # 支付参数体（二维码链接 / 调起参数 / 跳转 URL）
    payBodyType: str  # code_url / pay_info / redirect_url


__all__ = [
    "CommonParam",
    "DaxResult",
    "GoodsDetail",
    "PayParam",
    "PayResult",
    "TerminalInfo",
]
