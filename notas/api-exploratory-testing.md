# TESTE EXPLORATORIO DE API SERVEREST
- teste de exploração da API ServeRest "https://compassuol.serverest.dev/" na ordem em que eu fui testando 

---

## USUARIOS

- get /usuários
    - status: 200
    - retorna quantidade e array de usuarios sem autenticação
    - o body retorna de perigoso:
        - true para administrador, o que confirma que a conta tem acessos especiais de administrador
        - retorna email, senha que são dados sensíveis
        - creio que o id não deveria retornar sem auth, por se tratar de uma api ServeRest de estudos não sei se tem necessidade ou não.

- post /usuários
    - status 201
    - retorna mensagem de "cadastro realizado com sucesso" e o id do usuário
    - creio que talvez não deveria retornar o id do usuário por questões de segurança. por ser uma api ServeRest de estudos não sei se tem necessidade ou não.

- get /usuários{_id}
    - status 200
    - retorna o usuário corretamente
    - mesmos problemas de body que o /usuários

- delete /usuários
    - status 200
    - retorna mensagem "Registro excluído com sucesso"

- delete /usuários
    - status 200 
    - retorna mensagem "nenhum registro encontrado"

- put /usuários
    - status 200
    - retorna mensagem "Registro alterado com sucesso"
    - se tentar atualizar para um email já cadastrado:
        - status 400
        - "Este email já está sendo usado"
    - erro na rota put:
        - se tentar atualizar com id inexistente = retorna 201 created
            - deveria retornar algum erro 400 com usuário não encontrado, pois além de "desvio de função", isso pode gerar uma quantidade enorme de dados duplicados/errados nos bancos de dados

---

## LOGIN

- post /login (para fazer login)
    - status 200
    - retorna mensagem "login realizado com sucesso" e um token para auth

- post /login (com senha errada)
    - status 401
    - mensagem de email e/ou senha inválida
        (correto: importante não especificar qual dos dois está incorreto por medidas de segurança)
    
- post /login (sem campo body json)
    - satus 400 
    - mensagem de "email é obrigatório/password é obrigatório"

---

## PRODUTOS

- get /produtos
    - status 200
    - retorna quantidade de produtos cadastrados + array com nome/preço/descricao/quantidade/id dos produtos
    - problemas:
        - retorna quantidade de produtos cadastrados e dados sobre os produtos sem necessidade de auth. por se tratar de uma api de estudos, não sei se é o esperado ou não.

- get /produtos_id
    - status 200
    - mesmos problemas que do get/produtos

- get /produtos_id (inexistente)
    - status 400
    - retorna mensagem "produto não encontrado"

- post /produtos (sem token)
    - status 401
    - retorna mensagem "token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

- post /produtos (com token)
    - satus 201
    - retorna mensagem com "cadastro realizado com sucesso" + id do produto

- post /produtos (usuário admin=false)
    - status 403
    - retorna mensagem "rota exclusiva para administradores"

- post /produtos (já criado)
    - status 400
    - retorna mensagem "já existe produto com esse nome"

- put /produtos
    - status 200
    - retorna mensagem "registro alterado com sucesso"

- put /produtos (id inexistente + nome do produto existente)
    - status 400 
    - retorna mensagem "já existe produto com esse nome"
    - problemas
        - deveria retornar que o id/produto não existe em vez de "não existe produto com esse nome"

- put /produtos
    - status 201 
    - retorna mensagem "cadastro realizado com sucesso" + id do produto 
    - problemas
        - não deveria estar criando produtos nessa rota, apenas atualizando

- delete /produtos (sem token)
    - status 401
    - retorna mensagem "token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

- delete /produtos
    - status 200
    - retorna mensagem "registro exluído com sucesso"