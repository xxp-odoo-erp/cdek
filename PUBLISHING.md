# Инструкция по публикации пакета cdek

## Подготовка к публикации

1. Убедитесь, что вы находитесь в корневой директории проекта
2. Проверьте, что все файлы закоммичены в git:
   ```bash
   git status
   ```

## Тестирование сборки

Перед публикацией убедитесь, что пакет собирается без ошибок:

```bash
python3 -m pip install --upgrade build twine
python3 -m build
```

Это создаст два файла в директории `dist/`:
- `cdek-2.1.0.tar.gz` - исходный дистрибутив
- `cdek-2.1.0-py3-none-any.whl` - wheel дистрибутив

## Проверка пакета

Перед публикацией проверьте, что пакет установится и будет работать:

```bash
# Тестирование установки из локального wheel
python3 -m pip install dist/cdek-2.1.0-py3-none-any.whl --force-reinstall

# Проверка импорта
python3 -c "import cdek; print(cdek.__version__)"
python3 -c "from cdek import CdekClient; print('OK')"

# Удаление тестовой установки
python3 -m pip uninstall cdek -y
```

## Проверка метаданных

Проверьте содержимое файла METADATA:

```bash
unzip -c dist/cdek-2.1.0-py3-none-any.whl cdek-2.1.0.dist-info/METADATA
```

## Публикация в Test PyPI

Для проверки публикации сначала загрузите пакет в Test PyPI:

```bash
python3 -m twine upload --repository testpypi dist/*
```

Вам понадобится зарегистрироваться на https://test.pypi.org/account/register/ и создать токен API.

Для публикации используйте токен в формате: `__token__`

## Публикация в PyPI

После успешной проверки на Test PyPI, опубликуйте пакет в PyPI:

```bash
python3 -m twine upload dist/*
```

Вам понадобится зарегистрироваться на https://pypi.org/account/register/ и создать токен API.

### Создание токена API на PyPI

1. Зайдите на https://pypi.org/manage/account/token/
2. Создайте новый токен с правами на весь проект или на конкретный пакет
3. Скопируйте токен и используйте его для авторизации

### Авторизация

При публикации Twine попросит ввести логин и пароль:
- Username: `__token__`
- Password: ваш токен API

Или вы можете настроить `.pypirc` файл:

```ini
[pypi]
username = __token__
password = pypi-ваш-токен-здесь
```

## Проверка установки из PyPI

После публикации попробуйте установить пакет:

```bash
python3 -m pip install cdek
```

## Обновление версии

При каждом обновлении версии:

1. Обновите `__version__` в `cdek/__init__.py`
2. Обновите версию в `pyproject.toml`
3. Обновите версию в `setup.py`
4. Синхронизируйте `CHANGELOG.md` и руководство по публикации
5. Соберите новый пакет
6. Опубликуйте пакет

## Проверка опубликованного пакета

После публикации проверьте, что пакет доступен:
- https://pypi.org/project/cdek/
- https://test.pypi.org/project/cdek/

## Дополнительная информация

- [Документация Twine](https://twine.readthedocs.io/)
- [Документация по упаковке Python](https://packaging.python.org/)
- [PyPI](https://pypi.org/)

