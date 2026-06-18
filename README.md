# Testes automatizados da API ServeRest

Projeto desenvolvido para o desafio do bootcamp de QA da Compass UOL.

O objetivo deste projeto é automatizar testes da API ServeRest, cobrindo os principais cenários das rotas de usuários, login e produtos.

API utilizada: https://compassuol.serverest.dev/

## Tecnologias utilizadas

* Python
* Pytest
* Requests
* Postman
* Git e GitHub
* Claude
* ChatGPT
* Codex

## Estrutura do projeto

```text
api-test-bootcamp/
├── notas/
│   └── api-exploratory-testing.md
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_login.py
│   ├── test_produtos.py
│   └── test_usuarios.py
├── .gitignore
├── PLANO-DE-TESTES.md
├── README.md
└── requirements.txt
```

## Pré-requisitos

Para executar o projeto, é necessário ter instalado:

* Python
* Git

## Instalação

Clone o repositório:

```bash
git clone https://github.com/gustavolkbr/api-test-bootcamp.git
```

Entre na pasta do projeto:

```bash
cd api-test-bootcamp
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

No Windows, ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Execução dos testes

Para executar todos os testes:

```bash
pytest -v
```

Para executar somente os testes de usuários:

```bash
pytest -v tests/test_usuarios.py
```

Para executar somente os testes de login:

```bash
pytest -v tests/test_login.py
```

Para executar somente os testes de produtos:

```bash
pytest -v tests/test_produtos.py
```

Também é possível executar um teste específico:

```bash
pytest -v tests/test_usuarios.py::test_cadastrar_usuario_valido
```

## Cenários automatizados

A suíte possui 23 testes automatizados.

### Usuários

* Listar usuários.
* Cadastrar usuário com dados válidos.
* Cadastrar usuário com e-mail duplicado.
* Cadastrar usuário com campos obrigatórios faltando.
* Buscar usuário por ID válido.
* Buscar usuário por ID inexistente.
* Atualizar usuário.
* Atualizar usuário utilizando um e-mail já cadastrado.
* Excluir usuário.
* Excluir usuário com ID inexistente.

### Login

* Realizar login com credenciais corretas.
* Tentar realizar login com senha incorreta.
* Tentar realizar login com e-mail inexistente.
* Tentar realizar login com os campos vazios.

### Produtos

* Listar produtos.
* Cadastrar produto com token de administrador.
* Tentar cadastrar produto sem token.
* Tentar cadastrar produto com usuário não administrador.
* Buscar produto por ID válido.
* Buscar produto por ID inexistente.
* Atualizar produto.
* Excluir produto.
* Tentar excluir produto sem token.

## Organização e limpeza dos dados

Os usuários e produtos utilizados nos testes são criados de forma dinâmica.

Os e-mails e nomes dos produtos recebem um identificador gerado com `uuid4`, evitando conflito com registros que já existem na API.

As fixtures utilizam `yield` para separar a preparação e a limpeza dos dados. Os registros são criados antes da execução do teste e excluídos ao final, evitando o acúmulo de usuários e produtos no ambiente público.

O usuário administrador e seu token utilizam `scope="module"`. Dessa forma, eles são criados apenas uma vez durante o módulo que precisa desses dados, em vez de serem recriados para cada teste.

## Processo de desenvolvimento

* Primeiro, foram realizados testes manuais no Postman nas rotas de usuários, login e produtos. Durante essa etapa, foram verificados os códigos de status, mensagens e dados retornados pela API. 

* Os resultados dos testes manuais foram registrados no arquivo `notas/api-exploratory-testing.md` e utilizados como base para definir os cenários automatizados.

* O plano de testes foi criado com apoio do Claude, organizando o objetivo, a estratégia, o escopo, os cenários e os critérios de qualidade.

* O ChatGPT foi utilizado para ajudar na estruturação do projeto e na revisão das decisões tomadas durante o desenvolvimento.

* O ChatGPT e o Claude também foram utilizados como apoio na criação e revisão da documentação, ajudando a organizar as notas, o plano de testes e os relatórios gerados durante a exploração e o desenvolvimento da suíte.

* O Codex foi utilizado como apoio no desenvolvimento do código, principalmente para agilizar trechos repetitivos e manter um padrão entre os testes.

* Todos os testes foram executados pelo terminal. As falhas encontradas foram analisadas individualmente antes de qualquer alteração no código.

* No início, os usuários e produtos criados durante os testes permaneciam cadastrados na API. Para evitar esse problema, foram utilizadas fixtures com `yield`, realizando a exclusão dos registros depois de cada teste.

* Durante as primeiras execuções completas, um novo usuário administrador e um novo token eram criados para vários testes. Isso aumentava a quantidade de requisições e, em algumas execuções, a API retornava `503 Service Unavailable` ou deixava de reconhecer usuários e tokens recém-criados.

* Para reduzir a quantidade de requisições, as fixtures do usuário administrador e do token foram alteradas para `scope="module"`. Depois desse ajuste, a suíte passou a executar os 23 testes com sucesso e em menos tempo.

* Durante a revisão final, foi percebido que os testes de listagem verificavam apenas se algumas chaves existiam na resposta. Foram adicionadas validações com `type()` para confirmar que `quantidade` era um número inteiro e que `usuarios` e `produtos` eram listas.

* Também foram adicionadas requisições de busca depois dos cadastros e exclusões. Assim, os testes não validam apenas a mensagem de sucesso, mas também confirmam que o registro foi realmente criado ou removido.

* As ferramentas de inteligência artificial foram utilizadas como apoio. O código gerado foi revisado, executado e ajustado durante o desenvolvimento antes de ser enviado ao repositório.

## Cobertura dos testes

O método de cálculo foi baseado nos critérios apresentados no artigo indicado no desafio:

* `Path Coverage`, que verifica quais caminhos da API foram cobertos;
* `Operator Coverage`, que verifica quais operações HTTP foram cobertas;
* cobertura dos cenários definidos no plano de testes.

Também foi calculada uma cobertura funcional geral, considerando os quatro módulos apresentados na documentação da ServeRest.

### Cobertura funcional total

A documentação da ServeRest apresenta quatro grupos principais:

* Login
* Usuários
* Produtos
* Carrinhos

A suíte cobre três desses quatro grupos:

```text
3 grupos cobertos / 4 grupos existentes × 100 = 75%
```

**Cobertura funcional total atingida: 75%.**

Esse percentual representa a quantidade de módulos da ServeRest cobertos pelo projeto. O módulo de carrinhos não fazia parte do desafio e não foi automatizado.

### Path Coverage dentro do escopo

Dentro do escopo do desafio, foram considerados cinco paths:

* `/usuarios`
* `/usuarios/{_id}`
* `/login`
* `/produtos`
* `/produtos/{_id}`

Todos possuem testes automatizados:

```text
5 paths cobertos / 5 paths previstos no escopo × 100 = 100%
```

**Path Coverage dentro do escopo: 100%.**

### Operator Coverage dentro do escopo

Foram consideradas onze operações HTTP:

* `GET /usuarios`
* `POST /usuarios`
* `GET /usuarios/{_id}`
* `PUT /usuarios/{_id}`
* `DELETE /usuarios/{_id}`
* `POST /login`
* `GET /produtos`
* `POST /produtos`
* `GET /produtos/{_id}`
* `PUT /produtos/{_id}`
* `DELETE /produtos/{_id}`

Todas possuem pelo menos um teste automatizado:

```text
11 operações cobertas / 11 operações previstas no escopo × 100 = 100%
```

**Operator Coverage dentro do escopo: 100%.**

### Cobertura dos cenários planejados

O plano de testes definiu 23 cenários e todos foram implementados:

```text
23 cenários automatizados / 23 cenários planejados × 100 = 100%
```

**Cobertura dos cenários planejados: 100%.**

Os percentuais de 100% representam apenas o escopo de usuários, login e produtos. Eles não significam que toda a API ServeRest está coberta.

## Cenários fora da cobertura

O módulo de carrinhos não foi automatizado porque não fazia parte do escopo definido no desafio.

Também ficaram fora alguns cenários adicionais que poderiam aumentar a cobertura, como:

* cadastro e atualização de produtos com outras combinações de campos inválidos;
* cadastro e atualização de usuários com outras combinações de campos inválidos;
* teste de todos os valores possíveis para cada parâmetro;
* teste de todos os códigos de status possíveis em cada operação;
* validação de todas as propriedades possíveis dos corpos das respostas.

Esses cenários não foram incluídos porque o foco do projeto foi atender aos fluxos solicitados para usuários, login e produtos dentro do tempo disponível para a entrega.

## Bugs encontrados

Durante os testes exploratórios, foram encontrados comportamentos em que uma requisição de atualização utilizando um ID inexistente cria um novo registro.

* [PUT de usuário com ID inexistente cria um novo usuário](https://github.com/gustavolkbr/api-test-bootcamp/issues/1)
* [PUT de produto com ID inexistente cria um novo produto](https://github.com/gustavolkbr/api-test-bootcamp/issues/2)

Os passos para reprodução, resultados esperados e obtidos, severidade e evidências estão registrados nas Issues.

## Resultado da execução

A execução final da suíte apresentou:

```text
23 passed
```

Todos os testes foram executados com sucesso.
