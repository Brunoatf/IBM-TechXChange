import requests

class LLM:
    def __init__(self, api_key, project_id, model_id="mistralai/mistral-large"):
        self.api_key = api_key
        self.project_id = project_id
        self.model_id = model_id
        self.url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

        # Obter o access token usando a API Key
        self.access_token = self.get_access_token()

        # Configurar os headers com o access token obtido
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_access_token(self):
        token_url = "https://iam.cloud.ibm.com/identity/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code != 200:
            raise Exception(f"Falha ao obter o access token: {response.status_code} - {response.text}")
        access_token = response.json().get('access_token')
        return access_token

    def generate_text(self, prompt, max_new_tokens=2000, decoding_method="greedy", repetition_penalty=1.0):
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": decoding_method,
                "max_new_tokens": max_new_tokens,
                "repetition_penalty": repetition_penalty
            },
            "model_id": self.model_id,
            "project_id": self.project_id,
            "moderations": {
                "hap": {
                    "input": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {
                            "remove_entity_value": True
                        }
                    },
                    "output": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {
                            "remove_entity_value": True
                        }
                    }
                }
            }
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=body
        )

        if response.status_code != 200:
            raise Exception(f"Error in response: {response.status_code} - {response.text}")

        data = response.json()
        return data["results"][0]["generated_text"]
