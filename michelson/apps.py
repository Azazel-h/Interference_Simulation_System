from django.apps import AppConfig


class MichelsonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'michelson'
    column_names = (
        "Длина волны",
        "Длина 1 плеча",
        "Длина 2 плеча",
        "Отражаемость разделителя луча",
        "Наклон зеркала по X",
        "Наклон зеркала по Y",
        "фокусное расстояние",
        "Размер рисунка",
        "Разрешение",
    )
