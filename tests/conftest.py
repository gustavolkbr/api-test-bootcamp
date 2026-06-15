from uuid import uuid4

import pytest
import requests


@pytest.fixture(scope="session")
def url_base():
    return "https://compassuol.serverest.dev"


@pytest.fixture
def usuario(url_base):
    dados_usuario = {
        "nome": "Gustavo",
        "email": f"gustavo_{uuid4()}@email.com",
        "password": "teste",
        "administrador": "false",
    }

    resposta = requests.post(f"{url_base}/usuarios", json=dados_usuario)
    assert resposta.status_code == 201, resposta.text

    corpo = resposta.json()
    assert "_id" in corpo, resposta.text

    id_usuario = corpo["_id"]
    dados_usuario["_id"] = id_usuario

    yield dados_usuario

    if id_usuario:
        requests.delete(f"{url_base}/usuarios/{id_usuario}")


@pytest.fixture(scope="module")
def usuario_administrador(url_base):
    dados_usuario = {
        "nome": "Guilherme",
        "email": f"guilherme_{uuid4()}@email.com",
        "password": "teste",
        "administrador": "true",
    }

    resposta = requests.post(f"{url_base}/usuarios", json=dados_usuario)
    assert resposta.status_code == 201, resposta.text

    corpo = resposta.json()
    assert "_id" in corpo, resposta.text

    id_usuario = corpo["_id"]
    dados_usuario["_id"] = id_usuario

    yield dados_usuario

    if id_usuario:
        requests.delete(f"{url_base}/usuarios/{id_usuario}")


@pytest.fixture
def token_usuario(url_base, usuario):
    dados_login = {
        "email": usuario["email"],
        "password": usuario["password"],
    }

    resposta = requests.post(f"{url_base}/login", json=dados_login)
    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()
    assert "authorization" in corpo, resposta.text

    return corpo["authorization"]


@pytest.fixture(scope="module")
def token_administrador(url_base, usuario_administrador):
    dados_login = {
        "email": usuario_administrador["email"],
        "password": usuario_administrador["password"],
    }

    resposta = requests.post(f"{url_base}/login", json=dados_login)
    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()
    assert "authorization" in corpo, resposta.text

    return corpo["authorization"]


@pytest.fixture
def produto(url_base, token_administrador):
    dados_produto = {
        "nome": f"Teclado Husky {uuid4()}",
        "preco": 250,
        "descricao": "Teclado mecanico",
        "quantidade": 10,
    }
    cabecalho = {"Authorization": token_administrador}

    resposta = requests.post(
        f"{url_base}/produtos",
        json=dados_produto,
        headers=cabecalho,
    )
    assert resposta.status_code == 201, resposta.text

    corpo = resposta.json()
    assert "_id" in corpo, resposta.text

    id_produto = corpo["_id"]
    dados_produto["_id"] = id_produto

    yield dados_produto

    if id_produto:
        requests.delete(
            f"{url_base}/produtos/{id_produto}",
            headers=cabecalho,
        )
