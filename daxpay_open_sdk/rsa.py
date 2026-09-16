"""RSA 签名/验签 — SHA256withRSA，对照后端 RsaSignUtil

私钥 PKCS#8 PEM；公钥 X.509 PEM；数据显式 UTF-8；输出标准 Base64（非 URL-safe、无换行）。
"""
from __future__ import annotations

import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def rsa_sign(data: str, private_key_pem: str) -> str:
    """RSA 签名（SHA256withRSA，UTF-8，Base64 输出）— 对照后端 RsaSignUtil#sign"""
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"), password=None
    )
    signature = private_key.sign(
        data.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
    )
    return base64.b64encode(signature).decode("ascii")


def rsa_verify(data: str, sign_b64: str, public_key_pem: str) -> bool:
    """RSA 验签（SHA256withRSA）— 对照后端 RsaSignUtil#verify

    验签失败返回 False（不抛异常），便于调用方直接做布尔判定。
    """
    public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    try:
        public_key.verify(
            base64.b64decode(sign_b64),
            data.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False
