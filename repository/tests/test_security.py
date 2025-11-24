# tests/test_security.py
import pytest
from fastapi.routing import APIRoute
from app.main import app

client = None

@pytest.fixture(scope="module", autouse=True)
def setup_client():
    from fastapi.testclient import TestClient
    global client
    client = TestClient(app)

@pytest.mark.parametrize("route", [r for r in app.routes if isinstance(r, APIRoute)])
def test_protected_endpoints_require_auth(route):
    """Verifica que los endpoints que deben estar protegidos devuelvan 401 sin token."""
    if route.path in ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]:
        pytest.skip("Docs o esquema OpenAPI")

    # Filtramos endpoints públicos (si los tenés)
    public_routes = ["/", "/token", "/health"]
    if route.path in public_routes:
        pytest.skip(f"Ruta pública: {route.path}")

    # Tomamos un método válido
    method = list(route.methods - {"HEAD", "OPTIONS"})[0].lower()
    response = getattr(client, method)(route.path)

    # Algunos endpoints pueden requerir parámetros (los saltamos por ahora)
    if response.status_code == 422:  # faltan params
        pytest.skip(f"Faltan parámetros en {route.path}")

    assert response.status_code in [401, 403], f"{route.path} debería requerir autenticación, devolvió {response.status_code}"
