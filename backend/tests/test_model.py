import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from model import Image, SessionPreset

@pytest.fixture
def db_session():
    """Create a fresh in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()

def test_create_image(db_session):
    """Test that an Image can be created and queried."""
    image = Image(
        filename="test.jpg",
        filepath="/images/test.jpg",
        source="local"
    )
    db_session.add(image)
    db_session.commit()
    
    # Query it back
    result = db_session.query(Image).filter_by(filename="test.jpg").first()
    
    assert result is not None
    assert result.filename == "test.jpg"
    assert result.filepath == "/images/test.jpg"
    assert result.source == "local"
    assert result.uploaded_at is not None  # Should be auto-set

def test_create_session_preset(db_session):
    """Test that a SessionPreset can be created and queried."""
    preset = SessionPreset(
        name="Quick Warmup",
        image_count=10,
        duration_seconds=30
    )
    db_session.add(preset)
    db_session.commit()
    
    # Query it back
    result = db_session.query(SessionPreset).filter_by(name="Quick Warmup").first()
    
    assert result is not None
    assert result.name == "Quick Warmup"
    assert result.image_count == 10
    assert result.duration_seconds == 30