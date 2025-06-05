import pytest
from httpx import AsyncClient, ASGITransport
from main import app  # tu FastAPI app

@pytest.mark.asyncio
async def test_login_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/login", json={"username": "usuario1", "password": "password1"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_failure():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/login", json={"username": "usuario1", "password": "wrongpassword"})
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_pokemon_with_valid_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Obtener token
        login_response = await ac.post("/login", json={"username": "usuario1", "password": "password1"})
        token = login_response.json()["access_token"]

        # Llamar POST /pokemon con token y datos
        response = await ac.post("/pokemon",
                                json={"pokemons": ["pikachu"]},
                                headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        assert any(p.get("nombre") == "pikachu" for p in results)

@pytest.mark.asyncio
async def test_pokemon_without_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # POST /pokemon sin token
        response = await ac.post("/pokemon", json={"pokemons": ["pikachu"]})
        assert response.status_code == 403
