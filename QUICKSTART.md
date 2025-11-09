# Быстрый старт для публикации

## Созданные файлы

Библиотека готова к публикации! Были созданы следующие файлы:

### Конфигурация пакета
- `pyproject.toml` - современная конфигурация пакета
- `setup.py` - классическая конфигурация для обратной совместимости
- `MANIFEST.in` - описание файлов для включения в дистрибутив

### Документация
- `README.md` - описание библиотеки и примеры использования
- `PUBLISHING.md` - подробная инструкция по публикации
- `CHANGELOG.md` - история изменений
- `LICENSE` - MIT лицензия

### Инструменты
- `Makefile` - команды для сборки и публикации
- `.gitignore` - исключения для git
- `requirements.txt` - зависимости

### Собранные пакеты
В директории `dist/` находятся готовые к публикации файлы:
- `cdek-2.1.0.tar.gz` - исходный дистрибутив
- `cdek-2.1.0-py3-none-any.whl` - wheel дистрибутив

## Быстрая публикация

### 1. Установите необходимые инструменты

```bash
python3 -m pip install --upgrade build twine
```

### 2. Проверьте пакет

```bash
# Соберите пакет
make build

# Проверьте метаданные
make check

# Протестируйте установку
make test
```

### 3. Опубликуйте в Test PyPI (опционально)

```bash
make publish-test
```

### 4. Опубликуйте в PyPI

```bash
make publish
```

## Альтернативный способ без Makefile

```bash
# Сборка
python3 -m build

# Проверка
twine check dist/*

# Тестовая публикация
twine upload --repository testpypi dist/*

# Публикация
twine upload dist/*
```

## Важные заметки

1. Вам понадобится зарегистрироваться на PyPI: https://pypi.org/account/register/
2. Создайте токен API: https://pypi.org/manage/account/token/
3. При публикации используйте:
   - Username: `__token__`
   - Password: ваш токен API

## Удаление временных файлов

```bash
make clean
```

## Структура пакета

После установки пакет будет доступен как:

```python
from cdek import CdekClient
from cdek.exceptions import CdekRequestException
from cdek.apps.order import OrderRequest
# и т.д.
```

