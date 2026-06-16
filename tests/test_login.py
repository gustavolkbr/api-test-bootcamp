from uuid import uuid4

import requests


def test_login_com_credenciais_corretas(url_base, usuario):
    dados_login = {
        "email": usuario["email"],
        "password": usuario["password"],
    }

    resposta = requests.post(f"{url_base}/login", json=dados_login)

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Login realizado com sucesso"
    assert corpo["authorization"]


def test_login_com_senha_incorreta(url_base, usuario):
    dados_login = {
        "email": usuario["email"],
        "password": "senha_incorreta",
    }

    resposta_busca = requests.get(
        f"{url_base}/usuarios/{usuario['_id']}"
    )

    assert resposta_busca.status_code == 200, resposta_busca.text

    resposta = requests.post(f"{url_base}/login", json=dados_login)

    assert resposta.status_code == 401, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Email e/ou senha inválidos"


def test_login_com_email_inexistente(url_base):
    dados_login = {
        "email": f"messi_{uuid4()}@email.com",
        "password": "teste",
    }

    resposta = requests.post(f"{url_base}/login", json=dados_login)

    assert resposta.status_code == 401, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Email e/ou senha inválidos"


def test_login_com_campos_vazios(url_base):
    dados_login = {
        "email": "",
        "password": "",
    }

    resposta = requests.post(f"{url_base}/login", json=dados_login)

    assert resposta.status_code == 400, resposta.text

    corpo = resposta.json()

    assert corpo["email"] == "email não pode ficar em branco"
    assert corpo["password"] == "password não pode ficar em branco"
