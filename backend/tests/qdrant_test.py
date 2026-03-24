from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://3e8bdca6-c38a-4be4-b3b6-e6655a48a0a7.sa-east-1-0.aws.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Z1PM-ZE5LnzaBiiUqpsGx4lTTwS9EZmAN8qCRPUif-A",
)

print(qdrant_client.get_collections())