# TaskManager

FastAPI приложение для управления задачами со сгенерированной документацией.

### Запуск

Запустить сервер:

```bash
uvicorn app.main:app --app-dir ./ --reload
```

Открыть документацию:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

### Примеры запросов

Создать задачу:

```bash
curl -s -X POST "http://127.0.0.1:8000/tasks" -H "Content-Type: application/json" -d "{\"title\":\"Write API\",\"description\":\"demo\",\"priority\":1}"
```

Получить задачу:

```bash
curl -s "http://127.0.0.1:8000/tasks/1"
```

404 если задача не найдена:

```bash
curl -s -i "http://127.0.0.1:8000/tasks/999"
```