"""DaxPay SDK 客户端 — 对照 sdk-contract.md 第十节

执行链路：填充公共参数 → 序列化 → 对 JSON 报文签名 → POST → 按原始响应体验签 → 返回 DaxResult。
时间字段一律使用北京时间 `yyyy-MM-dd HH:mm:ss` 字面量（平台按报文规范字面量验签）。
"""
from __future__ import annotations

import json
import secrets
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from daxpay_open_sdk.config import Config
from daxpay_open_sdk.errors import DaxPayError, ErrorCode
from daxpay_open_sdk.models import DaxResult, PayParam
from daxpay_open_sdk.rsa import rsa_sign, rsa_verify
from daxpay_open_sdk.sign import build_sign_str

DEFAULT_TIMEOUT = 30000


def _now_beijing() -> str:
    """当前时间的北京时间字面量（yyyy-MM-dd HH:mm:ss）— 对照后端 @JsonFormat(GMT+8)"""
    beijing = datetime.now(timezone.utc) + timedelta(hours=8)
    return beijing.strftime("%Y-%m-%d %H:%M:%S")


class DaxPayClient:
    """DaxPay 开放接口客户端

    单实例可复用；配置见 [Config][daxpay_open_sdk.config.Config]。
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._service_url = config.service_url.rstrip("/")
        # 配置以毫秒计（与其它语言 SDK 对齐），urllib 需要秒
        self._timeout = (config.timeout or DEFAULT_TIMEOUT) / 1000

    def execute(self, path: str, param: Dict[str, Any]) -> DaxResult:
        """通用执行入口

        :param path: 接口路径，如 `/unipay/pay`
        :param param: 业务参数（键名即报文键名）
        :return: 平台响应（已验签、code 已确认为 0）
        :raises DaxPayError: HTTP 异常 / 验签失败 / 业务 code != 0
        """
        request_param: Dict[str, Any] = dict(param)
        # 注入公共字段（调用方已显式传入时不覆盖）
        request_param.setdefault("mchNo", self._config.mch_no)
        if self._config.app_id and "appId" not in request_param:
            request_param["appId"] = self._config.app_id
        request_param.setdefault("reqId", str(uuid.uuid4()))
        request_param.setdefault("reqTime", _now_beijing())
        request_param.setdefault("nonceStr", secrets.token_hex(16))

        # 走 JSON 签名路径：序列化 → 对 JSON 签名 → 注入 sign → 重新序列化发送
        json_for_sign = json.dumps(request_param, ensure_ascii=False)
        sign_str = build_sign_str(json_for_sign)
        request_param["sign"] = rsa_sign(sign_str, self._config.private_key)
        body = json.dumps(request_param, ensure_ascii=False).encode("utf-8")

        raw_body = self._post(self._service_url + path, body)

        result: DaxResult = json.loads(raw_body)
        # 用原始报文验签（不可先反序列化再签名，会丢精度与字面量格式）
        sign = result.get("sign")
        if sign and not rsa_verify(build_sign_str(raw_body), sign, self._config.public_key):
            raise DaxPayError(ErrorCode.SIGN_VERIFY_FAILED, "响应验签失败")

        code = result.get("code", -1)
        if code != ErrorCode.SUCCESS:
            raise DaxPayError(code, result.get("msg", ""))
        return result

    def pay(self, param: PayParam) -> DaxResult:
        """支付下单 — POST /unipay/pay"""
        return self.execute("/unipay/pay", dict(param))

    def verify_notice(self, raw_body: str) -> bool:
        """回调通知验签（原始 HTTP body 字符串）— 对照契约第八节"""
        try:
            obj = json.loads(raw_body)
        except (TypeError, ValueError):
            return False
        if not isinstance(obj, dict) or not obj.get("sign"):
            return False
        return rsa_verify(build_sign_str(raw_body), obj["sign"], self._config.public_key)

    def _post(self, url: str, body: bytes) -> str:
        """POST JSON 报文并返回原始响应文本"""
        request = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise DaxPayError(-1, f"HTTP {error.code}: {detail}") from error
        except urllib.error.URLError as error:
            raise DaxPayError(-1, f"请求失败: {error.reason}") from error


__all__ = ["DEFAULT_TIMEOUT", "DaxPayClient"]
