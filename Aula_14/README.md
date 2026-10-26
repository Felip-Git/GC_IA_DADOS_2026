
# Casa de Sucos API

API desenvolvida em Python com FastAPI para consultar informações
nutricionais de frutas e cadastrar sucos.

## Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- Requests
- API pública Fruityvice

## Funcionalidades

- Consultar frutas e obter nome, calorias e açúcar.
- Cadastrar sucos com uma ou mais frutas.
- Calcular o total de calorias e açúcar de cada suco.
- Listar os sucos cadastrados.
- Atualizar as frutas de um suco e recalcular os valores nutricionais.
- Tratar erros de frutas não encontradas e falhas na API externa.

## Instalação

1. Clone o repositório e acesse a pasta aula_14.
2. Crie um ambiente virtual:

   python -m venv venv

3. Ative o ambiente virtual.

   Windows PowerShell:

   .\venv\Scripts\Activate.ps1

4. Instale as dependências:

   pip install -r requirements.txt

## Execução

Execute o comando:

uvicorn main:app --reload

A API estará disponível em:

http://127.0.0.1:8000

## Documentação e testes

Acesse o Swagger para testar os endpoints:

http://127.0.0.1:8000/docs

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /frutas/{nome} | Consulta uma fruta |
| POST | /sucos | Cadastra um suco |
| GET | /sucos | Lista os sucos |
| PUT | /sucos/{id} | Atualiza as frutas de um suco |

## Cálculo nutricional

Para cada fruta, são considerados 100 g.
Os valores de calorias e açúcar são consultados na Fruityvice
e somados para obter os totais do suco.

## Armazenamento

Os sucos são armazenados temporariamente em memória.
Os dados são perdidos quando a aplicação é reiniciada.

## API externa

https://www.fruityvice.com/api/fruit/
