from dataclasses import dataclass, fields
from typing import get_args, get_origin


@dataclass
class Source:
    """Базовый класс для всех классов ответов"""

    @classmethod
    def from_dict(cls, properties: dict | None = None):
        """
        Формирует объект класса из ответа

        Args:
            properties: словарь свойств из ответа API

        Returns:
            Новый экземпляр класса с заполненными полями
        """
        if properties is None:
            return cls()

        # Обработка структуры с 'entity'
        if 'entity' in properties and isinstance(properties['entity'], (dict, list)):
            entity_data = properties['entity']
            # Проверяем если это список
            if isinstance(entity_data, list) and len(entity_data) > 1:
                if 'requests' in properties:
                    entity_data[0]['requests'] = properties.get('requests', [])
                properties = entity_data[0]
            elif isinstance(entity_data, dict):
                # Копируем данные из entity
                entity_dict = entity_data.copy()
                # Добавляем requests если есть на верхнем уровне
                if 'requests' in properties and 'requests' not in entity_dict:
                    entity_dict['requests'] = properties.get('requests', [])
                if 'related_entities' in properties and 'related_entities' not in entity_dict:
                    entity_dict['related_entities'] = properties.get('related_entities', [])
                properties = entity_dict

        # Обработка структуры type.entity
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

        # Создаём новый экземпляр класса через конструктор
        # Фильтруем только те поля, которые есть в dataclass
        dataclass_fields = {f.name for f in fields(cls)}
        filtered_properties = {k: v for k, v in properties.items() if k in dataclass_fields}
        return cls(**filtered_properties)

    def __setattr__(self, key, value):
        # Получаем описание поля (если оно есть)
        flds = {f.name: f.type for f in fields(self)}

        # Если поле определено в dataclass, обрабатываем его тип
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

            # Устанавливаем через super() для dataclass полей
            super().__setattr__(key, value)
        else:
            # Для неизвестных полей используем object.__setattr__
            object.__setattr__(self, key, value)
