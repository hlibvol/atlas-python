from app.db.application_urls.models import ApplicationUrl


def test_get_application_urls(
    client, test_application_url, superuser_token_headers
):
    response = client.get(
        "/api/v1/application-urls", headers=superuser_token_headers
    )
    assert response.status_code == 200
    app_url = response.json()[0]
    assert app_url["id"] == test_application_url.id
    assert app_url["name"] == test_application_url.name
    assert app_url["url"] == test_application_url.url
    assert app_url["description"] == test_application_url.description


def test_delete_application_url(
    client, test_application_url, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/application-urls/{test_application_url.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(ApplicationUrl).all() == []


def test_edit_application_url(
    client, test_application_url, superuser_token_headers
):
    new_application_url = {"name": "View Buton", "url": "viewbutton.com"}

    response = client.put(
        f"/api/v1/application-urls/{test_application_url.id}",
        json=new_application_url,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_application_url.id
    assert response.json()["name"] == new_application_url["name"]
    assert response.json()["url"] == new_application_url["url"]


def test_get_application_url(
    client,
    test_application_url,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/application-urls/{test_application_url.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_application_url.id
    assert response.json()["name"] == test_application_url.name
    assert response.json()["url"] == test_application_url.url
    assert response.json()["description"] == test_application_url.description
