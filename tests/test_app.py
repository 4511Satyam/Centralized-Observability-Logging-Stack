def test_imports():
    from app.main import app
    assert app.title == "Text Summarization Observability API"
