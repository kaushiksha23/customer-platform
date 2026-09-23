import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
)

from app import app


def test_customer_search():
    client = app.test_client()

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        (1, "Kaushik", "kaushik@example.com")
    ]

    mock_connection.cursor.return_value = mock_cursor

    with patch("app.get_db_connection", return_value=mock_connection):
        response = client.get("/customers/search?name=Kaushik")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["name"] == "Kaushik"
    assert data[0]["email"] == "kaushik@example.com"


def test_customer_search_without_name():
    client = app.test_client()

    response = client.get("/customers/search")

    assert response.status_code == 400