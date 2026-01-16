import wmill
import requests

def main(name: str, email: str, branche: str, challenge: str):
    """
    Интеграция с SeaTable через API v2.
    """
    # 1. Получаем API Token из переменных Windmill
    raw_token = wmill.get_variable("u/admin/SEATABLE_TOKEN")
    API_TOKEN = raw_token.strip()

    # 2. Получаем Access Token (Авторизация)
    auth_url = "https://cloud.seatable.io/api/v2.1/dtable/app-access-token/"
    auth_headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Accept": "application/json"
    }

    auth_response = requests.get(auth_url, headers=auth_headers)
    if auth_response.status_code != 200:
        return {"status": "error", "message": "Ошибка авторизации", "details": auth_response.text}

    auth_data = auth_response.json()
    access_token = auth_data.get("access_token")
    dtable_uuid = auth_data.get("dtable_uuid")

    # 3. Добавляем строку (API v2 через Gateway)
    add_row_url = f"https://cloud.seatable.io/api-gateway/api/v2/dtables/{dtable_uuid}/rows/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # ВАЖНО: передаем массив в "rows"
    payload = {
        "table_name": "Anfragen",
        "rows": [{
            "name": name,
            "email": email,
            "branche": branche,
            "herausforderung": challenge # сопоставляем переменную из Typebot
        }]
    }

    response = requests.post(add_row_url, json=payload, headers=headers)

    if response.status_code == 200:
        return {
            "status": "success",
            "message": "Данные в таблице!",
            "details": response.json()
        }
    else:
        return {
            "status": "error", 
            "http_code": response.status_code, 
            "response": response.text
        }