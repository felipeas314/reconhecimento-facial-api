# API de Reconhecimento Facial

API para cadastro e reconhecimento de faces usando FastAPI e Qdrant como banco de dados vetorial.

## Stack Tecnológica

- **FastAPI** - Framework web assíncrono
- **Qdrant** - Banco de dados vetorial para busca por similaridade
- **face_recognition** - Biblioteca de reconhecimento facial (baseada em dlib)
- **Docker** - Containerização

## Arquitetura

O projeto segue uma arquitetura em camadas inspirada em padrões como Clean Architecture:

```
reconhecimento-facial-api/
├── app.py                      # Entry point da aplicação
├── src/
│   ├── config/
│   │   ├── settings.py         # Configurações da aplicação
│   │   └── database.py         # Conexão com Qdrant
│   ├── routers/                # Controllers/Endpoints
│   │   ├── face_router.py      # Endpoints de face (/faces/*)
│   │   ├── health_router.py    # Health check
│   │   └── legacy_router.py    # Compatibilidade (/post-face, /check-face)
│   ├── services/               # Regras de negócio
│   │   └── face_service.py     # Lógica de reconhecimento
│   ├── repositories/           # Acesso a dados
│   │   └── face_repository.py  # Operações no Qdrant
│   └── schemas/                # DTOs/Models
│       └── face.py             # Request/Response models
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Camadas

| Camada | Responsabilidade | Equivalente Java |
|--------|------------------|------------------|
| **routers** | Receber requisições HTTP, validar entrada | @RestController |
| **services** | Regras de negócio, orquestração | @Service |
| **repositories** | Acesso a dados, queries | @Repository |
| **schemas** | DTOs, validação de dados | Records/DTOs |
| **config** | Configurações, conexões | @Configuration |

## Instalação

### Com Docker (recomendado)

```bash
docker-compose up -d
```

### Localmente

1. Inicie o Qdrant:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

2. Crie e ative uma virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie a API:
```bash
uvicorn app:app --reload --port 5001
```

## Endpoints

### Novos (RESTful)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/faces/register` | Cadastra uma nova face |
| POST | `/faces/recognize` | Reconhece uma face |
| GET | `/health` | Health check |

### Legacy (compatibilidade)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/post-face` | Cadastra uma nova face |
| POST | `/check-face` | Reconhece uma face |

### Exemplos

#### POST /faces/register
```bash
curl -X POST http://localhost:5001/faces/register \
  -F "label=Felipe" \
  -F "File1=@photo1.jpg" \
  -F "File2=@photo2.jpg" \
  -F "File3=@photo3.jpg"
```

#### POST /faces/recognize
```bash
curl -X POST http://localhost:5001/faces/recognize \
  -F "File1=@photo.jpg"
```

**Resposta:**
```json
{
  "result": [
    {"label": "Felipe", "distance": 0.029}
  ]
}
```

## Interpretação da Distância

| Distância | Interpretação |
|-----------|---------------|
| 0.0 - 0.1 | Match muito forte |
| 0.1 - 0.3 | Match bom |
| 0.3 - 0.5 | Match fraco |
| > 0.6 | Não considerado match |

## Configuração

Variáveis de ambiente (ou arquivo `.env`):

| Variável | Default | Descrição |
|----------|---------|-----------|
| `QDRANT_HOST` | localhost | Host do Qdrant |
| `QDRANT_PORT` | 6333 | Porta do Qdrant |

## Documentação Interativa

Com a API rodando, acesse:
- **Swagger UI:** http://localhost:5001/docs
- **ReDoc:** http://localhost:5001/redoc

## Dashboard do Qdrant

Visualize os dados armazenados em:
- http://localhost:6333/dashboard
