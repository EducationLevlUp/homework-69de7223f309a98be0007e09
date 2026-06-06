# Deep Research Virtual Files Agent

Поисковый агент на основе архитектуры курса [Deep Agents from Scratch](https://github.com/langchain-ai/deep-agents-from-scratch).

## Возможности

- **Поиск в интернете** — интеграция с DuckDuckGo через LangChain search tools
- **Виртуальные файлы** — в-memory файловая система через `StateBackend` (thread-scoped)
- **Экспорт в реальную ФС** — автоматическая выгрузка виртуальных файлов после завершения работы агента

## Архитектура

```
agent/
  core.py          # Инициализация агента, StateBackend, регистрация инструментов
  export_hook.py   # Пост-обработка: синхронизация StateBackend → реальная ФС
tools/
  search.py        # Обёртка search-инструмента
config/
  settings.py      # Загрузка настроек из env vars
main.py            # Точка входа: запуск агента + экспорт результатов
```

## Настройка

1. Скопируйте `.env.example` в `.env` и заполните необходимые значения:
   ```bash
   cp .env.example .env
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Укажите API-ключ LLM-провайдера (например, `OPENAI_API_KEY`).

## Запуск

```bash
python main.py
```

Агент запустит интерактивный сеанс: вы можете задавать вопросы, и агент будет искать информацию в интернете, создавать виртуальные файлы с результатами и, по завершении, экспортировать их в директорию `./exported_files/`.

## Как это работает

1. **StateBackend** — в-memory хранилище файлов, привязанное к `thread_id`. Файлы существуют только в рамках сессии агента.
2. **Search tool** — `DuckDuckGoSearchResults` из LangChain, не требует API-ключа.
3. **Export hook** — после завершения работы агента (`/exit` или ошибка) содержимое StateBackend записывается в реальную директорию.

## Тестирование

```bash
python -m pytest tests/ -v
```

Тесты используют моки для LLM и search-инструментов, поэтому не требуют внешних API.

## Допущения

- **Виртуальные файлы** реализованы через `StateBackend` (in-memory, thread-scoped storage).
- **LLM по умолчанию**: `openai:gpt-4o` (конфигурируемо через `LLM_MODEL`).
- **Search provider**: DuckDuckGo (бесплатный, без ключа).
- **Путь экспорта**: `./exported_files/` (конфигурируемо через `EXPORT_DIR`).
