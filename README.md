# Serai 后端技术测试 (FastAPI)

用于支持前端 Demo 运行的后端服务。

## 环境要求
- Python 3.10+

## 本地运行

### 安装与配置
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### 启动服务
```powershell
uvicorn app.main:app --reload
```

启动后访问：

* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)（Swagger 文档）

## 接口说明

### GET /health

健康检查，返回服务状态。

响应示例：

```json
{"status":"ok","version":"0.1.0"}
```

### POST /generate

根据品牌、活动、上下文生成摘要、风险与建议。

请求体示例：

```json
{"brand":"Nike","event":"Launch","context":"Hello"}
```

成功响应示例（当前为 stub）：

```json
{
  "summary":"stub summary",
  "risks":["stub risk 1","stub risk 2"],
  "recommendation":"stub recommendation"
}
```

校验失败示例（例如缺少 `context`）：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "invalid request body",
    "request_id": "..."
  }
}
```

## 设计说明

* 使用 FastAPI + Pydantic 做请求/响应与 schema 校验
* `/generate` 使用内存 TTL 缓存：key = SHA256(brand|event|context)，最多 1000 条、过期时间 10 分钟，避免重复生成、降低延迟与成本
* 分层结构：
  * `app/api` 路由
  * `app/schemas` 请求/响应模型
  * `app/services` 业务逻辑（生成器、缓存）
  * `app/core` 配置（环境变量）
* 请求 ID 中间件：自动生成或透传 `X-Request-Id`，并在响应中返回，便于排查
* 统一错误响应格式（含 code、message、request_id）

## 配置项

环境变量说明见 `.env.example`：

* `GENERATOR_MODE`：`mock` | `llm`，当前默认 mock
* `LLM_API_KEY`：仅在 `llm` 模式下需要，不在代码中硬编码

## 若有更多时间会做的改进

* 接入真实 LLM 客户端，并加上超时、重试、熔断
* 缓存可扩展为 Redis 或分布式方案
* 增加限流与请求体大小限制
* 补充更多测试用例（pytest）与覆盖率
* 基于样本数据做简单 RAG（分块、向量检索、pgvector），并做效果与成本评估
