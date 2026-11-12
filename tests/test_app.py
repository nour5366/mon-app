
from unittest.mock import MagicMock, patch
from app import app


def test_accueil():
    conn = MagicMock()
    cur = MagicMock()

    conn.__enter__.return_value = conn
    conn.cursor.return_value.__enter__.return_value = cur
    cur.fetchone.return_value = (1,)

    with patch("app.get_connection", return_value=conn):
        client = app.test_client()
        response = client.get("/")

    assert response.status_code == 200
    assert b"Bonjour !" in response.data
    assert b"1 fois" in response.data


def test_insertion_visite():
    conn = MagicMock()
    cur = MagicMock()

    conn.__enter__.return_value = conn
    conn.cursor.return_value.__enter__.return_value = cur
    cur.fetchone.return_value = (2,)

    with patch("app.get_connection", return_value=conn):
        client = app.test_client()
        client.get("/")

    cur.execute.assert_any_call("INSERT INTO visites DEFAULT VALUES")
    cur.execute.assert_any_call("SELECT COUNT(*) FROM visites")

