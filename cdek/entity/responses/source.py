from dataclasses import dataclass, fields
from typing import get_args, get_origin


@dataclass
class Source:
    """Базовый класс для всех классов ответов"""

    def __init__(self, properties=None):
        """Инициализация объекта из словаря свойств"""
        # Сначала вызываем dataclass __init__ для установки значений по умолчанию
        super().__init__()

        # Инициализируем атрибуты из properties
        if properties is not None:
            # Обработка структуры с 'entity' (первый приоритет - API может вернуть просто entity)
            if 'entity' in properties and isinstance(properties['entity'], dict):
                entity_data = properties['entity']
                # Проверяем если это список
                if isinstance(entity_data, list) and len(entity_data) > 1:
                    if 'requests' in properties:
                        entity_data[0]['requests'] = properties.get('requests', [])
                    properties = entity_data[0]
                elif isinstance(entity_data, dict):
                    # Копируем данные из entity
                    entity_dict = entity_data.copy()
                    # Добавляем requests если есть на верхнем уровне (в properties, не в entity)
                    if 'requests' in properties and 'requests' not in entity_dict:
                        entity_dict['requests'] = properties.get('requests', [])
                    if 'related_entities' in properties and 'related_entities' not in entity_dict:
                        entity_dict['related_entities'] = properties.get('related_entities', [])
                    # ВАЖНО: заменяем properties на entity_dict полностью
                    properties = dict(entity_dict)  # Создаем новый словарь

            # Обработка структуры type.entity (для некоторых ответов API)
            # Проверяем после обработки entity
            elif 'type' in properties and isinstance(properties['type'], dict):
                type_data = properties['type']
                if 'entity' in type_data and isinstance(type_data['entity'], dict):
                    # Берем данные из type.entity
                    entity_data = type_data['entity'].copy()
                    # Добавляем requests если есть
                    if 'requests' in type_data:
                        entity_data['requests'] = type_data['requests']
                    if 'related_entities' in type_data:
                        entity_data['related_entities'] = type_data.get('related_entities', [])
                    # Используем entity_data для заполнения
                    properties = entity_data

            # Заполнение свойств из словаря
            for key, value in properties.items():
                if not key.startswith('_'):
                    # Не устанавливаем 'type' если это словарь с entity - это уже обработано
                    if key == 'type' and isinstance(value, dict) and 'entity' in value:
                        # Пропускаем это поле, оно уже обработано выше
                        continue
                    setattr(self, key, value)

    @classmethod
    def from_dict(cls, properties: dict | None = None):
        """
        Формирует объект класса из ответа

        Args:
            properties: словарь свойств из ответа API

        Returns:
            Новый экземпляр класса с заполненными полями
        """
        # Создаём новый экземпляр класса через конструктор
        return cls(properties)

    def __setattr__(self, key, value):
        # Получаем описание поля (если оно есть)
        flds = {f.name: f.type for f in fields(self)}
        if key in flds:
            expected_type = flds[key]
            origin = get_origin(expected_type)

            # ✅ Если это список других dataclass
            if origin is list or origin is list:
                inner_type = get_args(expected_type)[0]
                if isinstance(value, list) and hasattr(
                    inner_type, "__dataclass_fields__"
                ):
                    value = [
                        inner_type(**v) if isinstance(v, dict) else v for v in value
                    ]

            # ✅ Если это dataclass
            elif hasattr(expected_type, "__dataclass_fields__") and isinstance(
                value, dict
            ):
                value = expected_type(**value)

        super().__setattr__(key, value)
