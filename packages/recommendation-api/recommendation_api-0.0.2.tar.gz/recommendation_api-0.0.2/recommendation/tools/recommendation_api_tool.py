from promptflow import tool
import requests
import json


@tool
def get_recommendation_api(recommendation_api_url: str):
    url = recommendation_api_url
    headers = {
        "requestId": "test_request_id",
        "country": "uk",
        "num": "20",
        "Content-Type": "application/json",
    }

    try:
        payload = {"pageType": "chatbot", "guid": "abcde12345"}
    except json.JSONDecodeError:
        print("Invalid JSON input")
        return {"error": "Invalid JSON input"}

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": "Request failed",
            "status_code": response.status_code,
            "response_text": response.text,
        }
