"""DaxPay Open SDK for Python — 包根

对齐 `--_doc/design/sdk-contract.md` 第十节三件套：Config / DaxPayClient / SignUtil。
"""
from daxpay_open_sdk.client import DaxPayClient
from daxpay_open_sdk.config import Config
from daxpay_open_sdk.errors import DaxPayError, ErrorCode
from daxpay_open_sdk.models import (
    CommonParam,
    DaxResult,
    GoodsDetail,
    PayParam,
    PayResult,
    TerminalInfo,
)
from daxpay_open_sdk.rsa import rsa_sign, rsa_verify
from daxpay_open_sdk.sign import build_sign_str

__version__ = "1.0.0"

__all__ = [
    "CommonParam",
    "Config",
    "DaxPayClient",
    "DaxPayError",
    "DaxResult",
    "ErrorCode",
    "GoodsDetail",
    "PayParam",
    "PayResult",
    "TerminalInfo",
    "build_sign_str",
    "rsa_sign",
    "rsa_verify",
]
