import pytest
from images import get_random_images
from model import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

@pytest.fixture
def db_session():
    """Create a fresh in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def temp_image_dir(tmp_path):
    """Create a temporary directory with test images."""
    # Create a fake image file
    test_image = tmp_path / "test.jpg"
    test_image.write_bytes(b"fake image content")
    return tmp_path

def test_get_random_images_returns_requested_count(db_session):
    """Test that get_random_images returns the requested number of images."""
    # Add some images to the database
    for i in range(5):
        image = Image(
            filename=f"test{i}.jpg",
            filepath=f"/fake/path/test{i}.jpg",
            source="local"
        )
        db_session.add(image)
    db_session.commit()
    
    # Request 3 random images
    result = get_random_images(db_session, 3)
    
    assert len(result) == 3

def test_get_random_images_empty_database(db_session):
    """Test that get_random_images returns empty list when no images exist."""
    result = get_random_images(db_session, 5)
    
    assert result == []

def test_get_random_images_requests_more_than_available(db_session):
    """Test that requesting more images than available returns all images."""
    # Add only 2 images
    for i in range(2):
        image = Image(
            filename=f"test{i}.jpg",
            filepath=f"/fake/path/test{i}.jpg",
            source="local"
        )
        db_session.add(image)
    db_session.commit()
    
    # Request 10 images
    result = get_random_images(db_session, 10)
    
    assert len(result) == 2  # Should only return what's available

def test_get_random_images_requests_more_than_available(db_session):
    """Test that requesting more images than available returns all images."""
    # Add only 2 images
    for i in range(2):
        image = Image(
            filename=f"test{i}.jpg",
            filepath=f"/fake/path/test{i}.jpg",
            source="local"
        )
        db_session.add(image)
    db_session.commit()
    
    # Request 10 images
    result = get_random_images(db_session, 10)
    
    assert len(result) == 2  # Should only return what's available