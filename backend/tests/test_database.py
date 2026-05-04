from database import engine, SessionLocal, get_db

def test_engine_connects():
    """Verify the engine can establish a connection."""
    connection = engine.connect()
    assert connection is not None
    connection.close()