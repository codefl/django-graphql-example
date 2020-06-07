import requests

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

url = 'http://127.0.0.1:8088/graphql'
r = requests.post(url, json={'query': query}, headers={
    "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZyYW5rIiwiZXhwIjoxNTkxNTcwMDkzLCJvcmlnSWF0IjoxNTkxNTY5NzkzfQ.fkWKGIV4-EieTeoFhEG10SnkR6snyNjgdk1GgTTur_8"
})
print(r.status_code)
print(r.text)
