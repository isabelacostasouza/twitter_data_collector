PREPARANDO O AMBIENTE
1. Instalar a biblioteca OAuth no computador (pip3 install oauth2)

CONSEGUINDO SUAS CHAVES DE ACESSO
1. Entrar e logar em 'developer.twitter.com'
2. Selecionar a aba 'apps' e 'criar app'
3. Ao criar as configurações do app, clicar em 'gerar token'
4. Você agora tem suas chaves de acesso :)

FAZENDO O CÓDIGO DE COLETA (coleta_iterativa.py)
1. Importe as bibliotecas JSON e OAuth2 para o seu projeto .py
2. Inicialize suas chaves como variáveis 
3. Inicialize as variáveis consumer e token da biblioteca oauth usando suas chaves
4. Inicialize seu cliente a partir das variáveis inicializadas pelo oauth
5. Crie uma requisição na URL de coleta da API, adicionando como query a palavra que deseja pesquisar
6. Decodifique os dados da requisição com a função .decode()
7. Inicialize um objeto JSON para os dados decodificados
8. Sua coleta está pronta! Só falta filtrar, se você quiser :)
