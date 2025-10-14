# 🗓️ Sistema de Reservas / Agendamento

Um sistema simples para criar, visualizar e reservar horários.

---

## 🌟 Visão Geral
Este projeto é um sistema de reservas/slots que permite:

- Criar horários disponíveis
- Reservar slots
- Evitar conflitos de horário
- Listar todas as reservas via API
- (Futuro) Cancelar ou editar reservas

**Tecnologias utilizadas:**

- **Backend:** Python, FastAPI, Tortoise ORM, SQLite  
- **Frontend:** HTML, CSS, JS (consome API)  
- **Documentação automática:** Swagger UI (`/docs`)  

---

## 📂 Estrutura de Arquivos

    reservation_system/
    ├── backend/
    │ ├── main.py # Inicializa FastAPI + Tortoise ORM
    │ ├── models.py # Modelos de dados (Slot)
    │ ├── schemas.py # Pydantic models para request/response
    │ ├── crud.py # Funções async de CRUD
    │ └── database.py # Configuração do Tortoise ORM
    ├── frontend/
    │ ├── index.html # Página principal com calendário/lista de horários
    | ├── styles.css # CSS para estilizar
    │ └── app.js # JS para consumir a API
    ├── data/ # Pasta para banco SQLite persistente
    └── README.md # Esta documentação

---

## 📝 Modelos de Dados

**Slot (Tabela/Modelo)**  

| Campo     | Tipo       | Descrição                          |
|-----------|-----------|-----------------------------------|
| id        | int       | Identificador único               |
| date      | date      | Data do slot                      |
| hour      | time      | Hora do slot                       |
| duration  | int       | Duração em minutos                |
| status    | str       | "available" ou "reserved"         |

**Pydantic Schemas (Request/Response)**

```python
from pydantic import BaseModel
from datetime import date, time

class SlotCreate(BaseModel):
    date: date
    hour: time
    duration: int

class SlotOut(BaseModel):
    id: int
    date: date
    hour: time
    duration: int
    status: str

    model_config = {
        "from_attributes": True  # substitui orm_mode para Pydantic v2
    }
```

## ⚡ Endpoints da API
|Método	 |Endpoint    |Descrição	                   |Request Body |Response          |
|--------|------------|------------------------------|-------------|------------------|
|GET	   |/slots	    |Lista todos os slots          |	-	         |List[SlotOut]     |
|POST	   |/slots	    |Cria um novo slot	           |SlotCreate   |SlotOut           |
|GET	   |/slots/{id}	|Busca slot específico pelo ID |	-	         |SlotOut           |
|PUT	   |/slots/{id}	|Atualiza um slot              |SlotCreate   |SlotOut           |
|DELETE	 |/slots/{id}	|Remove um slot                |	-          |{"msg": "deleted"}|


### 🔄 Fluxo do Backend

`main.py` inicializa FastAPI e conecta ao banco via Tortoise ORM.

`models.py` define o modelo Slot.

`schemas.py` define os Pydantic models para requisições e respostas.

`crud.py` implementa funções assíncronas como:

    create_slot(data: SlotCreate)

    get_slots()

    get_slot(id: int)

    update_slot(id: int, data: SlotCreate)

    delete_slot(id: int)

Endpoints chamam as funções do crud.py e retornam JSON.

## 🧪 Testando a API

FastAPI gera documentação interativa automática em:
`http://127.0.0.1:8000/docs`

Para rodar o backend:

    # Ativar virtualenv
    `source venv/Scripts/activate`  # Windows
    # ou
    `source venv/bin/activate`      # Linux/Mac
    
    # Rodar servidor
    `uvicorn backend.main:app --reload`
    
Acesse a documentação do Swagger e teste os endpoints.

## 💾 Banco de Dados

Banco em SQLite.

Para persistência:

Coloque o arquivo db.sqlite3 dentro da pasta data/

Configure Tortoise ORM para usar sqlite://data/db.sqlite3

Durante desenvolvimento, é possível usar banco em memória para testes rápidos:

    TORTOISE_ORM = {
        "connections": {"default": "sqlite://:memory:"},
        "apps": {
            "models": {
                "models": ["backend.models"],
                "default_connection": "default",
            },
        },
}

<div align="center"> <p>Desenvolvido por João P. Soares 🧑‍💻</p> </div>

