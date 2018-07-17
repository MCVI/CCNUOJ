from src import create_app


__all__ = ['app']

app = create_app(module_name=__name__)
