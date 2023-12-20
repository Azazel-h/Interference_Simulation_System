from django.apps import AppConfig


class VisualizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fabry_perot'
    column_names = (
        "Длина волны",
        "Разница длин волн",
        "Расстояние между зеркалами",
        "Фокусное расстояние линзы",
        "Коэффициент отражения",
        "Показатель преломления",
        "Размер рисунка",
        "Разрешение",
    )
