# Plano de testes - API ServeRest

## 1. Objetivo da suíte

Como proposto no desafio, o objetivo desta suíte é validar o funcionamento dos endpoints da API ServeRest (https://compassuol.serverest.dev/) relacionados às rotas de usuários, login e produtos.

A suíte deve verificar respostas de sucesso e erro, incluindo códigos de status HTTP, mensagens retornadas e dados presentes no corpo da resposta.

Os testes automatizados também devem garantir que os cenários sejam independentes, utilizem dados dinâmicos quando necessário e possam ser executados repetidamente sem depender de registros criados manualmente.

## 2. Estratégia

Os testes serão feitos diretamente na API, sem uso de interface gráfica.

Para isso, será utilizado Python com Pytest para organizar e executar os testes, além da biblioteca Requests para enviar as requisições HTTP para a ServeRest.

As validações serão feitas principalmente pelo código de status da resposta, pelas mensagens retornadas e pelos dados presentes no corpo da resposta.

Serão testados cenários de sucesso e de erro. Quando necessário, serão usados dados dinâmicos para evitar conflito com registros já existentes na API.

## 3. Escopo

A suíte irá cobrir os endpoints de usuários, login e produtos da API ServeRest.

Nos testes de usuários, serão validados os fluxos de listagem, cadastro, busca por ID, atualização e exclusão.

Nos testes de login, serão validados os cenários de credenciais corretas, senha incorreta, e-mail inexistente e campos vazios.

Nos testes de produtos, serão validados os fluxos de listagem, cadastro com e sem autenticação de administrador, busca por ID, atualização e exclusão.

Não fazem parte deste desafio testes de interface gráfica, desempenho, segurança aprofundada ou acesso ao banco de dados da aplicação.

## 4. Cenários de teste

### 4.1 Usuários
Listar usuários cadastrados.
Cadastrar um usuário com dados válidos.
Tentar cadastrar um usuário com e-mail já utilizado.
Tentar cadastrar um usuário com campos obrigatórios faltando.
Buscar um usuário por ID válido.
Buscar um usuário por ID inexistente.
Atualizar os dados de um usuário existente.
Tentar atualizar um usuário utilizando um e-mail já cadastrado.
Excluir um usuário existente.
Tentar excluir um usuário com ID inexistente.

### 4.2 Login
Realizar login com e-mail e senha corretos.
Tentar realizar login com senha incorreta.
Tentar realizar login com e-mail inexistente.
Tentar realizar login com os campos vazios.

### 4.3 Produtos
Listar os produtos cadastrados.
Cadastrar um produto com token de usuário administrador.
Tentar cadastrar um produto sem token de autenticação.
Tentar cadastrar um produto com usuário que não seja administrador.
Buscar um produto por ID válido.
Buscar um produto por ID inexistente.
Atualizar um produto existente.
Excluir um produto existente.
Tentar excluir um produto sem token de autenticação.

## 5. Critérios de qualidade

Um teste será considerado pronto quando:

possuir um nome que deixe claro o cenário testado;
puder ser executado sem depender da ordem dos outros testes;
utilizar dados criados pelo próprio teste quando necessário;
validar o código de status retornado;
validar a mensagem ou os dados principais presentes na resposta;
poder ser executado mais de uma vez sem gerar conflito com dados já existentes;
realizar a limpeza dos dados criados quando isso for necessário;
apresentar um resultado fácil de entender em caso de falha.

## 6. Itens fora do escopo

Nesta etapa, não serão realizados:

testes de interface gráfica;
testes de desempenho ou carga;
testes de segurança aprofundados;
validações diretamente no banco de dados;
testes dos endpoints de carrinhos;
validação de todos os campos possíveis de todas as respostas;
testes em outros ambientes além do ambiente público da ServeRest.

Esses itens ficaram fora do escopo por não fazerem parte do desafio proposto e pelo tempo disponível para a entrega.

## 7. Possíveis riscos

Durante a execução dos testes, alguns cenários podem falhar por causa de dados já existentes na API, instabilidade do ambiente ou alterações feitas por outros usuários.

Para reduzir esse risco, serão utilizados dados dinâmicos, principalmente nos campos de e-mail e nome de produto.

Também será necessário garantir que usuários e produtos criados durante os testes sejam excluídos quando possível.