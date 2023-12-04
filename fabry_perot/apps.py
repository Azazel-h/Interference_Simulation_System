from django.apps import AppConfig


class VisualizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fabry_perot'
    column_names = (
        "Длина волны",
        "Расстояние между стеклами",
        "Фокусное расстояние линзы",
        "Разница хода",
        "Коэффициент отражения",
        "Коэффициент преломления",
        "Размер рисунка",
        "Разрешение",
    )
