# Biblioteca Infantil

Aplicação web para catalogar livros e materiais de leitura para crianças, com interface simples e API REST em Flask.

## Funcionalidades

- Listagem de livros
- Busca por título ou autor
- Filtro por categoria
- Cadastro de novos livros
- Edição de livros existentes
- Exclusão de livros
- Banco SQLite local
- Frontend em HTML/CSS/JavaScript

## Estrutura do projeto

- `app.py` – backend Flask, modelagem e rotas da API
- `index.html` – interface da biblioteca
- `biblioteca.db` – banco de dados SQLite gerado automaticamente
- `requirements.txt` – dependências do projeto

## Como executar

1. Entre na pasta do projeto:
   ```bash
   cd caminho/da/biblioteca_infantil
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   python -m pip install -r requirements.txt
   ```

4. Inicie a aplicação:
   ```bash
   python app.py
   ```

5. Abra no navegador do computador que está executando o servidor:
   ```text
   http://127.0.0.1:5000
   ```

6. Para permitir acesso de outros computadores na mesma rede:

   - descubra o IP local do computador servidor (`ipconfig` no Windows ou `ip addr` no Linux/macOS);
   - inicie o servidor e libere a porta 5000 no firewall, se solicitado;
   - nos outros computadores, abra o endereço abaixo usando o IP do servidor:

   ```text
   http://SEU_IP_LOCAL:5000
   ```
   Exemplo: http://192.168.0.15:5000

> O servidor foi configurado para aceitar conexões externas com `host='0.0.0.0'`.
> O endereço `127.0.0.1` funciona somente no próprio computador servidor.

Para usar a biblioteca pela internet, é necessário publicar esta aplicação em um servidor ou serviço de hospedagem. Um endereço local não fica acessível automaticamente fora da rede.

É possível escolher outro endereço ou porta sem editar o código:

```bash
set HOST=0.0.0.0
set PORT=8080
python app.py
```

## API

### Listar livros
```http
GET /api/livros
```

### Buscar livros
```http
GET /api/livros?busca=lobato
```

### Filtrar por categoria
```http
GET /api/livros?categoria=Infantojuvenil
```

### Obter livro por ID
```http
GET /api/livros/<id>
```

### Cadastrar livro
```http
POST /api/livros
Content-Type: application/json

{
  "titulo": "Livro de teste",
  "autor": "Autor de teste",
  "categoria": "Geral",
  "descricao": "Descrição do livro",
  "arquivo_url": "https://example.com/livro.pdf"
}
```

### Atualizar livro
```http
PUT /api/livros/<id>
Content-Type: application/json
```

### Excluir livro
```http
DELETE /api/livros/<id>
```

## Observações

- O banco de dados é criado automaticamente ao iniciar a aplicação.
- O primeiro acesso insere um exemplo inicial de livro.
- A aplicação foi pensada para uso local e desenvolvimento.
