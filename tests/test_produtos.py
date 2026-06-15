from uuid import uuid4

import requests


def test_listar_produtos(url_base):
    resposta = requests.get(f"{url_base}/produtos")

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert "quantidade" in corpo
    assert "produtos" in corpo
    assert type(corpo["quantidade"]) == int
    assert type(corpo["produtos"]) == list
    assert corpo["quantidade"] == len(corpo["produtos"])


def test_cadastrar_produto_com_token_administrador(
    url_base,
    token_administrador,
):
    dados_produto = {
        "nome": f"Mouse Redragon {uuid4()}",
        "preco": 150,
        "descricao": "Mouse gamer",
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
    id_produto = corpo.get("_id")

    assert corpo["message"] == "Cadastro realizado com sucesso"
    assert id_produto

    resposta_busca = requests.get(f"{url_base}/produtos/{id_produto}")
    assert resposta_busca.status_code == 200, resposta_busca.text

    produto_cadastrado = resposta_busca.json()

    assert produto_cadastrado["_id"] == id_produto
    assert produto_cadastrado["nome"] == dados_produto["nome"]
    assert produto_cadastrado["preco"] == dados_produto["preco"]
    assert produto_cadastrado["descricao"] == dados_produto["descricao"]
    assert produto_cadastrado["quantidade"] == dados_produto["quantidade"]

    requests.delete(
        f"{url_base}/produtos/{id_produto}",
        headers=cabecalho,
    )


def test_cadastrar_produto_sem_token(url_base):
    dados_produto = {
        "nome": f"Microfone Maono {uuid4()}",
        "preco": 300,
        "descricao": "Microfone USB",
        "quantidade": 5,
    }

    resposta = requests.post(f"{url_base}/produtos", json=dados_produto)

    assert resposta.status_code == 401, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == (
        "Token de acesso ausente, inválido, expirado "
        "ou usuário do token não existe mais"
    )


def test_cadastrar_produto_com_usuario_nao_administrador(
    url_base,
    token_usuario,
):
    dados_produto = {
        "nome": f"Mouse Redragon {uuid4()}",
        "preco": 150,
        "descricao": "Mouse gamer",
        "quantidade": 10,
    }
    cabecalho = {"Authorization": token_usuario}

    resposta = requests.post(
        f"{url_base}/produtos",
        json=dados_produto,
        headers=cabecalho,
    )

    assert resposta.status_code == 403, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Rota exclusiva para administradores"


def test_buscar_produto_por_id_valido(url_base, produto):
    resposta = requests.get(f"{url_base}/produtos/{produto['_id']}")

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert corpo["_id"] == produto["_id"]
    assert corpo["nome"] == produto["nome"]
    assert corpo["preco"] == produto["preco"]


def test_buscar_produto_por_id_inexistente(url_base):
    id_inexistente = "1234567812345678"

    resposta = requests.get(f"{url_base}/produtos/{id_inexistente}")

    assert resposta.status_code == 400, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Produto não encontrado"


def test_atualizar_produto(url_base, produto, token_administrador):
    dados_atualizados = {
        "nome": f"Microfone Maono {uuid4()}",
        "preco": 300,
        "descricao": "Microfone USB",
        "quantidade": 5,
    }
    cabecalho = {"Authorization": token_administrador}

    resposta = requests.put(
        f"{url_base}/produtos/{produto['_id']}",
        json=dados_atualizados,
        headers=cabecalho,
    )

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Registro alterado com sucesso"

    resposta_busca = requests.get(f"{url_base}/produtos/{produto['_id']}")
    assert resposta_busca.status_code == 200, resposta_busca.text

    produto_atualizado = resposta_busca.json()

    assert produto_atualizado["nome"] == dados_atualizados["nome"]
    assert produto_atualizado["preco"] == dados_atualizados["preco"]


def test_excluir_produto(url_base, produto, token_administrador):
    cabecalho = {"Authorization": token_administrador}

    resposta = requests.delete(
        f"{url_base}/produtos/{produto['_id']}",
        headers=cabecalho,
    )

    assert resposta.status_code == 200, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == "Registro excluído com sucesso"

    resposta_busca = requests.get(f"{url_base}/produtos/{produto['_id']}")
    assert resposta_busca.status_code == 400, resposta_busca.text

    corpo_busca = resposta_busca.json()

    assert corpo_busca["message"] == "Produto não encontrado"


def test_excluir_produto_sem_token(url_base, produto):
    resposta = requests.delete(f"{url_base}/produtos/{produto['_id']}")

    assert resposta.status_code == 401, resposta.text

    corpo = resposta.json()

    assert corpo["message"] == (
        "Token de acesso ausente, inválido, expirado "
        "ou usuário do token não existe mais"
    )
