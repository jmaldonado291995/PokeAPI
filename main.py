from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List, Dict
import httpx

# Claves JWT
SECRET_KEY = "secret123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

# Usuarios hardcodeados
fake_users = {
    "usuario1": "password1",
    "usuario2": "password2"
}

app = FastAPI(title="PokéAPI Auth", description="Reto Técnico", version="1.0")
token_auth_scheme = HTTPBearer()  # ✅ Reemplazamos OAuth2PasswordBearer

# Crear JWT Token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verificar JWT Token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token = credentials.credentials  # Extraemos el token del encabezado Bearer
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# Endpoint de login
@app.post("/login")
def login(data: Dict[str, str]):
    username = data.get("username")
    password = data.get("password")
    if fake_users.get(username) == password:
        token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

# Obtener evoluciones
async def get_evolution_chain(chain_url: str) -> List[str]:
    async with httpx.AsyncClient() as client:
        res = await client.get(chain_url)
        res.raise_for_status()
        chain_data = res.json()["chain"]

    def traverse(chain):
        names = [chain["species"]["name"]]
        for evo in chain["evolves_to"]:
            names.extend(traverse(evo))
        return names

    return traverse(chain_data)

# Consultar pokemones
@app.post("/pokemon")
async def get_pokemons(data: Dict[str, List[str]], token: dict = Depends(verify_token)):
    results = []
    pokemons = data.get("pokemons", [])

    async with httpx.AsyncClient() as client:
        for name in pokemons:
            try:
                res = await client.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
                res.raise_for_status()
                p_data = res.json()

                species_url = p_data["species"]["url"]
                s_res = await client.get(species_url)
                s_res.raise_for_status()
                evo_url = s_res.json()["evolution_chain"]["url"]

                evolution_chain = await get_evolution_chain(evo_url)

                results.append({
                    "name": p_data["name"],
                    "height": p_data["height"],
                    "weight": p_data["weight"],
                    "types": [t["type"]["name"] for t in p_data["types"]],
                    "evolution_chain": evolution_chain
                })

            except httpx.HTTPStatusError:
                results.append({"name": name, "error": "Pokémon no encontrado"})

    return results
