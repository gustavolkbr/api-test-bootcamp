from uuid import uuid4

import requests


def test_listar_usuarios(url_base):
    resposta = requests.get(f"{url_base}/usuarios")

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert "quantidade" in corpo
    assert "usuarios" in corpo
    assert type(corpo["quantidade"]) == int
    assert type(corpo["usuarios"]) == list
    assert corpo["quantidade"] == len(corpo["usuarios"])


def test_cadastrar_usuario_valido(url_base):
    dados_usuario = {
        "nome": "Gustavo",
        "email": f"gustavo_{uuid4()}@email.com",
        "password": "teste",
        "administrador": "false",
    }

    resposta = requests.post(f"{url_base}/usuarios", json=dados_usuario)
    assert resposta.status_code == 201, resposta.text

    corpo = resposta.json()
    id_usuario = corpo.get("_id")

    assert corpo["message"] == "Cadastro realizado com sucesso"
    assert id_usuario

    resposta_busca = requests.get(f"{url_base}/usuarios/{id_usuario}")
    assert resposta_busca.status_code == 200, resposta_busca.text

    usuario_cadastrado = resposta_busca.json()

    assert usuario_cadastrado["_id"] == id_usuario
    assert usuario_cadastrado["nome"] == dados_usuario["nome"]
    assert usuario_cadastrado["email"] == dados_usuario["email"]

    requests.delete(f"{url_base}/usuarios/{id_usuario}")


def test_cadastrar_email_duplicado(url_base, usuario):
    dados_usuario = {
        "nome": "Messi",
        "email": usuario["email"],
        "password": "teste",
        "administrador": "false",
    }

    resposta = requests.post(f"{url_base}/usuarios", json=dados_usuario)

    assert resposta.status_code == 400, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Este email já está sendo usado"


def test_cadastrar_usuario_com_campos_faltando(url_base):
    dados_usuario = {
        "nome": "Gustavo",
        "email": f"gustavo_{uuid4()}@email.com",
    }

    resposta = requests.post(f"{url_base}/usuarios", json=dados_usuario)

    assert resposta.status_code == 400, resposta.text

    corpo = resposta.json()

    assert corpo["password"] == "password é obrigatório"
    assert corpo["administrador"] == "administrador é obrigatório"


def test_buscar_usuario_por_id_valido(url_base, usuario):
    resposta = requests.get(f"{url_base}/usuarios/{usuario['_id']}")

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert corpo["_id"] == usuario["_id"]
    assert corpo["nome"] == usuario["nome"]
    assert corpo["email"] == usuario["email"]


def test_buscar_usuario_por_id_inexistente(url_base):
    id_inexistente = "1234567812345678"

    resposta = requests.get(f"{url_base}/usuarios/{id_inexistente}")

    assert resposta.status_code == 400, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Usuário não encontrado"


def test_atualizar_usuario(url_base, usuario):
    dados_atualizados = {
        "nome": "Messi",
        "email": f"messi_{uuid4()}@email.com",
        "password": "teste",
        "administrador": "false",
    }

    resposta = requests.put(
        f"{url_base}/usuarios/{usuario['_id']}",
        json=dados_atualizados,
    )

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Registro alterado com sucesso"

    resposta_busca = requests.get(f"{url_base}/usuarios/{usuario['_id']}")
    assert resposta_busca.status_code == 200, resposta_busca.text

    usuario_atualizado = resposta_busca.json()

    assert usuario_atualizado["nome"] == dados_atualizados["nome"]
    assert usuario_atualizado["email"] == dados_atualizados["email"]
    assert (
        usuario_atualizado["password"]
        == dados_atualizados["password"]
    )
    assert (
        usuario_atualizado["administrador"]
        == dados_atualizados["administrador"]
    )


def test_atualizar_usuario_para_email_duplicado(
    url_base,
    usuario,
    usuario_administrador,
):
    dados_atualizados = {
        "nome": usuario["nome"],
        "email": usuario_administrador["email"],
        "password": usuario["password"],
        "administrador": usuario["administrador"],
    }

    resposta = requests.put(
        f"{url_base}/usuarios/{usuario['_id']}",
        json=dados_atualizados,
    )

    assert resposta.status_code == 400, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Este email já está sendo usado"


def test_excluir_usuario(url_base, usuario):
    resposta = requests.delete(f"{url_base}/usuarios/{usuario['_id']}")

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Registro excluído com sucesso"

    resposta_busca = requests.get(f"{url_base}/usuarios/{usuario['_id']}")
    assert resposta_busca.status_code == 400, resposta_busca.text

    corpo_busca = resposta_busca.json()

    assert corpo_busca["message"] == "Usuário não encontrado"


def test_excluir_usuario_com_id_inexistente(url_base):
    id_inexistente = "1234567812345678"

    resposta = requests.delete(f"{url_base}/usuarios/{id_inexistente}")

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Nenhum registro excluído"
