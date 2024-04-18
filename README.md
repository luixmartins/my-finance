# My Finance API 


My Finance é um projeto construído com Django REST Framework, desenvolvido para permitir que usuários registrem seus gastos de forma eficiente. Este projeto foi criado para fins de estudos do framework em questão. 

## A aplicação consiste em dois aplicativos principais: 

* User app - Responsável pelo gerenciamento de usuários.
    * Registro de usuários. 
    * Autenticação com token. 

* Finance app - Lida com o controle dos gastos dos usuários.   
    * Registro e gerenciamento de categorias de gastos. 
    * Registro de gastos associados a categorias e usuários. 

## Tecnologias Utilizadas 
* Django REST Framework 
* Docker para contêinarização da aplicação 

## Instruções de Uso 
### Pré-Requisitos
Para executar este projeto de forma eficiente, é necessário ter o Docker instalado em seu ambiente. Consulte a documentação oficial do Docker. 

### Executando o Projeto 
* Clone o repositório para o seu ambiente local. 
* Na raiz do projeto, execute o comando `docker-compose up`. Este comando construirá os contêineres necessários e iniciará o servidor. 
* Após a inicialização, a aplicação estará disponível em `http://localhost:8000/`

## Autenticação 

O projeto utiliza **Token Authentication** para garantir a segurança dos endpoints. Para acessar todos os recursos do app Finance, é necessário incluir o token de autenticação no cabeçalho das requisições, uma vez que cada gasto está associado a um usuário. 

## Estrutura do Banco de Dados 

O banco de dados é composto por três tabelas principais: 
    
* Users   
    * username 
    * email
    * password 

* Categories 
    * name 
    * user (referência tabela Users)
* Spends 
    * description 
    * value 
    * date 
    * created_at (read_only)
    * updated_at (read_only)
    * recurring 
    * period 

    **Obs*** É possível criar gastos recorrentes, neste caso o atributo ``recurring ``e ``period`` são opcionais. 
    
## ENDPOINTS 

### Users app 

* Criar usuário 
    * Método: ``POST``
    * URL: `/account/register/`
    * Formato: ``JSON``
    * Parâmetros 
        * ``username`` 
        * ``email``
        * `password`

* Logar usuário 
    * Método: ``POST``
    * URL: `/account/login/`
    * Formato: ``JSON``
    * Parâmetros 
        * ``username`` 
        * `password`

### Finance app 
#### **OBS** - Para todos os endpoints a seguir é necessário incluir o token de autenticação do usuário no cabeçalho da requisição. 

* Criar categoria 
    * Método: ``POST``
    * URL: `/finance/categories/`
    * Formato: ``JSON``
    * Parâmetros 
        * ``name`` 

* Listar todas as categorias
    * Método: ``GET``
    * URL: `/finance/categories/`
    * Formato: ``JSON``
    * Resposta: 
        * `id`
        * ``name`` 

* Criar novo gasto 
    * Método: ``POST``
    * URL: `/finance/spends/`
    * Formato: ``JSON``
    * Exemplo de entrada 
        ~~~json 
        "category": {
            "name": "gym"
        },
        "value": "120.00",
        "description": "Monthly payment for training at the gym",
        "date": "2024-04-09",
        "recurring": true, 
        "period": 30      
    É importante ressaltar que o exemplo cria um gasto recorrente. Portanto, o atributo **period** indica a quantidade de dias para a próxima recorrência. Por outro lado, para criar um gasto comum (não recorrente) basta não informar os campos **recurring** e **period**. 

* Listar todos os gastos
    * Método: ``GET``
    * URL: `/finance/spends/`
    * Formato: ``JSON``
    * Exemplo de saída 
        ~~~json 
        [
            {
                "id": 1,
                "category": {
                    "id": 1,
                    "name": "gym"
                },
                "value": "120.00",
                "description": "Monthly payment for training at the gym",
                "date": "2024-01-10",
                "created_at": "2024-04-18T19:44:27.883491Z",
                "updated_at": "2024-04-18",
                "recurring": true,
                "period": 30
            },
        ]
    * Filtros: 
        * Opções: `month=<int>`, `year=<int>`, `recurring=<boolean>`
        * URL: `finance/spends/?opções`

    É importante ressaltar que quando este endpoint é chamado, é verificado se existem gastos recorrentes para serem lançados de acordo com a data especificada. Caso os mesmos não existam, são criados os novos gastos. 

* Listar gasto específico 
    * Método: ``GET``
    * URL: `/finance/spends/<int:pk>`
    * Formato: ``JSON``
    * Exemplo de saída 
        ~~~json 
        {
            "id": 1,
            "category": {
                "id": 1,
                "name": "gym"
            },
            "value": "120.00",
            "description": "Monthly payment for training at the gym",
            "date": "2024-01-10",
            "created_at": "2024-04-18T19:44:27.883491Z",
            "updated_at": "2024-04-18",
            "recurring": true,
            "period": 30
        }

* Atualizar gasto
    * Método: ``PUT``
    * URL: `/finance/spends/<int:pk>`
    * Formato: ``JSON``
    * Exemplo de entrada 
        ~~~json 
        {
            "category": {
                "name": "gym - updated"
            },
            "value": "120.00",
            "description": "Monthly payment for training at the gym - updated",
            "date": "2024-01-10",
            "recurring": false,
            "period": null 
        }
    Quando é realizado a atualização da categoria, é verificado se ela já existe e está atribuída ao usuário, caso não, é criado uma nova categoria. 
    
    Para a atualização de recorrência, todos os gastos relacionados a este têm a recorrência desabilidata, assim como o atributo **period** é definido como nulo. 

* Apagar gasto
    * Método: ``DELETE``
    * URL: `/finance/spends/<int:pk>`
    
    Remove um gasto específico. 
