# tests/conftest.py
import sys, os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# 👇 Esto asegura que Python pueda encontrar el paquete "app"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importamos la aplicación FastAPI principal
from app.main import app

@pytest.fixture(scope="module")
def client():
    """Crea un cliente de test para FastAPI"""
    return TestClient(app)

@pytest.fixture
def mock_token_verification():
    """Simula la verificación del token de Firebase (para tests sin conexión real)"""
    with patch("firebase_admin.auth.verify_id_token") as mock_verify:
        mock_verify.return_value = {"user_id": "test_user"}
        yield
