from openai import OpenAI

client=OpenAI(
    api_key="ak-18919ed5ea5ee9b50f05c3e69df1f182",
    base_url="https://maas-api.cn-huabei-1.xf-yun.com/v2"
)
response=client.embeddings.create(
    model="xop3qwen8bembedding",
    input="Aileron hinge locations are very close to but aft of the center of gravity"
)

vector=response.data[0].embedding
print("向量维度:",len(vector))
print("前10个数字:",vector[:10])