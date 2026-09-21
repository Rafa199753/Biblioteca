import requests

BASE_URL = "http://127.0.0.1:5000"


def testar_listar():
    response = requests.get(f"{BASE_URL}/api/livros")
    print("LISTAR:", response.status_code)
    print(response.json())


def testar_busca():
    response = requests.get(f"{BASE_URL}/api/livros?busca=lobato")
    print("BUSCA:", response.status_code)
    print(response.json())


def testar_categoria():
    response = requests.get(f"{BASE_URL}/api/livros?categoria=Infantojuvenil")
    print("CATEGORIA:", response.status_code)
    print(response.json())


def testar_por_id():
    response = requests.get(f"{BASE_URL}/api/livros/1")
    print("POR_ID:", response.status_code)
    print(response.json())


def testar_criar():
    payload = {
        "titulo": "Livro de teste",
        "autor": "Autor de teste",
        "categoria": "Geral",
        "descricao": "Descrição de teste",
        "arquivo_url": "https://example.com/livro-teste.pdf"
    }
    response = requests.post(f"{BASE_URL}/api/livros", json=payload)
    print("CRIAR:", response.status_code)
    print(response.json())


def testar_atualizar():
    payload = {
        "titulo": "Livro atualizado",
        "autor": "Autor atualizado",
        "categoria": "Educativo",
        "descricao": "Descrição atualizada",
        "arquivo_url": "https://example.com/livro-atualizado.pdf"
    }
    response = requests.put(f"{BASE_URL}/api/livros/1", json=payload)
    print("ATUALIZAR:", response.status_code)
    print(response.json())


def testar_excluir():
    response = requests.delete(f"{BASE_URL}/api/livros/1")
    print("EXCLUIR:", response.status_code)
    print(response.json())


if __name__ == "__main__":
    testar_listar()
    testar_busca()
    testar_categoria()
    testar_por_id()
    testar_criar()
    testar_atualizar()
    testar_excluir()
