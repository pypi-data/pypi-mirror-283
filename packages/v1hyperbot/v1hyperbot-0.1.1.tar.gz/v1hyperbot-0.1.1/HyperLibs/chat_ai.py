import requests


class Chat:
    def gpt(self, question):
        response = requests.get(f"https://chatgpt.apinepdev.workers.dev/?question={question}")
        return response.json()["answer"] if "answer" in response.json() else "api sedang error"

    def gemini(self, question):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key=AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": question}]}],
            "generationConfig": {"temperature": 1, "topK": 0, "topP": 0.95, "maxOutputTokens": 8192, "stopSequences": []},
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Failed to generate content. Status code: {response.status_code}"
