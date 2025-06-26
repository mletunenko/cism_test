<h1>Cервис для асинхронной обработки задач с возможностью масштабирования и 
отказоустойчивости</h1>

Используемые ехнологии

	•	Язык программирования: Python 3.12
	•	База данных: PostgreSQL 14+
	•	Очередь сообщений: RabbitMQ
	•	Web Framework: FastAPI
	•	ORM: SQLAlchemy
	•	Система миграций: Alembic
	•	API документация: OpenAPI (Swagger)

API Endpoints

	•	POST /api/v1/tasks - создание задачи
	•	GET /api/v1/tasks - получение списка задач с фильтрацией и пагинацией
	•	GET /api/v1/tasks/{task_id} - получение информации о задаче
	•	DELETE /api/v1/tasks/{task_id} - отмена задачи
	•	GET /api/v1/tasks/{task_id}/status - получение статуса задачи