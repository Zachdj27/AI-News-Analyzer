import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_get_company_news():
    params = {
        "symbol": "AAPL",  
        "from": "2024-12-02",  
        "to": "2024-12-03",  
    }

    try:
        response = httpx.get(f"{BASE_URL}/company-news", params=params)
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            print("Response JSON:", response.json())
        else:
            print("Error Response:", response.text)

    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")

test_get_company_news()
