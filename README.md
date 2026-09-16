# DaxPay Open SDK for Python

DaxPay 开放支付平台 Python SDK，封装支付下单、关闭、退款、订单查询与回调验签。

> **适配 DaxPay Open ≥ 1.0** · **Python 3.10+** · LGPL-3.0 · 依赖 `cryptography`（RSA 签名），HTTP 走标准库 `urllib`

## 功能

- RSA 双向签名（SHA256withRSA，`cryptography` PKCS#1 v1.5），自动签名请求 / 验签响应与回调
- 走 JSON 签名路径，与开源版后端 `reqTime`（北京时间字面量）契约对齐
- 核心支付接口：pay / close / refund / query pay-order / query refund-order
- 异步回调验签
- 完整类型标注（`TypedDict` / `dataclass`）

## 安装（源码引入）

```bash
pip install git+https://github.com/opendaxpay/dax-pay-sdk-python.git
```

```python
from daxpay_open_sdk import Config, DaxPayClient, DaxPayError
```

## 快速开始

```python
client = DaxPayClient(
    Config(
        service_url="https://sandbox.daxpay.cn",
        mch_no="M200000001",
        app_id="APP001",
        private_key=merchant_private_key_pem,   # PEM 文本（PKCS#8）
        public_key=platform_public_key_pem,     # PEM 文本（X.509）
        timeout=30000,
    )
)

# 支付下单
result = client.pay({
    "bizOrderNo": "PAY20250805001",
    "title": "测试商品",
    "amount": 100,             # 分
    "method": "wechat_qr",
    "notifyUrl": "https://example.com/notify",
})
print(result["data"]["payBody"])

# 回调验签
# ok = client.verify_notice(raw_body)
```

## 测试

```bash
python -m unittest discover -s tests -t . -v
```

黄金向量（`tests/test_golden_vector.py`）与后端签名契约同源断言，V1/V2/V3 三组向量要求签名串与
RSA 签名值**字节级相等**（见 [`_doc/design/sdk-test-vectors.md`](https://gitee.com/dromara/dax-pay)）。

## 接口文档

- [接入准备](https://doc.open.daxpay.cn/api/getting-started) · [签名规则](https://doc.open.daxpay.cn/api/signature)
- 黄金测试向量：见 [`tests/test_golden_vector.py`](tests/test_golden_vector.py)（与后端签名契约同源断言）

## License

LGPL-3.0，与主仓库 [DaxPay Open](https://gitee.com/dromara/dax-pay) 同协议。
