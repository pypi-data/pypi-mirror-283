from src.pg_fms import create_app


def test_create_app():
    assert create_app() is not None
