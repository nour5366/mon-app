
from app import app, init_db, get_connection


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "OK"


def test_database_connection():
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        result = cur.fetchone()

    assert result[0] == 1
    conn.close()


def test_init_db():
    init_db()

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            "SELECT to_regclass('public.visites')"
        )
        result = cur.fetchone()

    assert result[0] == "visites"
    conn.close()


def test_home():
    init_db()

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert "Cette page a été visitée" in response.get_data(as_text=True)

