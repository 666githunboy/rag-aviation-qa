# RAG 航空维修文档问答

基于 RAG 的航空维修手册问答，覆盖 PDF 解析、文本切分、向量化、余弦检索、生成回答。

## 技术栈

- Python、pypdf、numpy
- 讯飞星辰 MaaS：Embedding（768 维）+ 对话模型
- 切分：chunk_size=500，chunk_overlap=50
- 检索：余弦相似度，top_k=5

## 运行

1. `pip install pypdf numpy openai`
2. 设置环境变量 `XFYUN_API_KEY`、`XFYUN_BASE_URL`
3. 运行主脚本

## 关键设计

- **目录过滤**：正则识别连续点号 + 页码格式，段数从 427 降到 204
- **页码追溯**：切分时存 `(页码, 文字)`，检索结果带来源页
- **失败调整**：top_k=3 时副翼段被切掉，扩到 top_k=5 后回答完整
- **context 清理**：压缩连续空白，避免模型被碎片干扰而拒答

## 已知问题

- 模型偶尔在资料外补充常识性描述，后续可加引用校验