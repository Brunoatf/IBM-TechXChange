import requests

class LLM:
    def __init__(self, access_token, project_id, model_id="ibm/granite-13b-chat-v2"):
        self.url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        self.access_token = access_token
        self.project_id = project_id
        self.model_id = model_id
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

    def generate_text(self, prompt, max_new_tokens=200, repetition_penalty=1.0, decoding_method="greedy"):
        body = {
            "parameters": {
                "decoding_method": decoding_method,
                "max_new_tokens": max_new_tokens,
                "repetition_penalty": repetition_penalty
            },
            "model_id": self.model_id,
            "project_id": self.project_id,
            "prompt": prompt,
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
            raise Exception("Erro na requisição: " + str(response.text))

        data = response.json()
        return data


# Exemplo de uso:
# Substitua 'YOUR_ACCESS_TOKEN' e 'YOUR_PROJECT_ID' pelos valores corretos
access_token = ""
project_id = ""
llm = LLM(access_token, project_id)
prompt = "Olá, tudo bem?"
resposta = llm.generate_text(prompt)
print(resposta)
