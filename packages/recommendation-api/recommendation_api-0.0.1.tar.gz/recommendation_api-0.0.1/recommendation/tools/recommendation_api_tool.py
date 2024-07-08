from promptflow import tool
import requests
import json


@tool
def get_recommendation_api():
    url = "http://k8s-eksrecommendergro-5887642276-2114908543.ap-northeast-2.elb.amazonaws.com/prodrec/recommendation"
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
