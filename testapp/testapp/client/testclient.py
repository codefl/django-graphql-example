from testapp.client.client import GQLClient


query = """
{
  products {
    id
    name
    variations {
      id
      variation
      currency
      price
    }
    tags {
      id
      name
      description
    }
  }
}
"""

client = GQLClient('http://127.0.0.1:8088/graphql')
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZyYW5rIiwiZXhwIjoxNTkxNTcwMDkzLCJvcmlnSWF0IjoxNTkxNTY5NzkzfQ.fkWKGIV4-EieTeoFhEG10SnkR6snyNjgdk1GgTTur_8"
res = client.query(query=query, token=token)
print(res)
