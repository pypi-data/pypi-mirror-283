from promptflow import tool
import requests
import json


@tool
def get_recommendation_api(
    http_method: str,
    api_url: str,
    content_type: str,
    requestId: str,
    country: str,
    num: str,
    pageType: str,
    guid: str,
):
    url = api_url
    headers = {
        "requestId": requestId,
        "country": country,
        "num": num,
        "Content-Type": content_type,
    }

    try:
        payload = {"pageType": pageType, "guid": guid}
    except json.JSONDecodeError:
        print("Invalid JSON input")
        return {"error": "Invalid JSON input"}

    if http_method.upper() == "POST":
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    else:
        return {"error": "Unsupported HTTP method"}

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": "Request failed",
            "status_code": response.status_code,
            "response_text": response.text,
        }
