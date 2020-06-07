import requests


class GQLClientException(Exception):

    def __init__(self, status_code, error_message):
        super()
        self.status_code = status_code
        self.error_message = error_message


class GQLClient:

    def __init__(self, url):
        self.url = url

    def mutate(self, mutation, variables=None, token=None):
        json_data = {
            'mutation': mutation
        }
        if variables is not None:
            json_data['variables'] = variables

        return self._execute(json_data, token)

    def query(self, query, variables=None, token=None):
        json_data = {
            'query': query
        }
        if variables is not None:
            json_data['variables'] = variables

        return self._execute(json_data, token)

    def _execute(self, json_data, token=None):
        if token is None:
            r = requests.post(self.url, json=json_data)
        else:
            r = requests.post(self.url, json=json_data, headers={
                "Authorization": "JWT " + token
            })

        if r.status_code != 200:
            raise GQLClientException(r.status_code, r.text)

        return r.text
