import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "https://api.instafill.ai/v1/forms"

class InstaFillClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("INSTAFILL_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as a parameter or in the .env file")

    def create_form(self, data, content_type="application/json"):
        headers = {"Content-Type": content_type, "x-api-key": self.api_key}
        if content_type == "application/json":
            response = requests.post(BASE_URL, headers=headers, json=data)
        elif content_type == "application/octet-stream":
            response = requests.post(BASE_URL, headers=headers, data=data)
        else:
            raise ValueError("Unsupported content type")
        response.raise_for_status()
        return response.json()

    def get_form(self, form_id):
        url = f"{BASE_URL}/{form_id}"
        headers = {"x-api-key": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def list_forms(self):
        headers = {"x-api-key": self.api_key}
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_form(self, form_id, data):
        url = f"{BASE_URL}/{form_id}"
        headers = {"x-api-key": self.api_key}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()