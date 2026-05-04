import pytest
from datetime import datetime, UTC
from pydantic import ValidationError

from schemas import ImageOut, SessionPresetOut, SessionPresetCreate

def test_image_out_valid():
    """Test ImageOut with valid data."""
    data = {
        "id": 1,
        "filename": "test.jpg",
        "source": "local",
        "uploaded_at": datetime.now(UTC)
    }
    image = ImageOut(**data)
    
    assert image.id == 1
    assert image.filename == "test.jpg"

def test_image_out_missing_field():
    """Test that missing required fields raise ValidationError."""
    data = {
        "id": 1,
        "filename": "test.jpg"
        # missing source and uploaded_at
    }
    
    with pytest.raises(ValidationError):
        ImageOut(**data)

def test_session_preset_create_valid():
    """Test SessionPresetCreate with valid data."""
    preset = SessionPresetCreate(
        name="Quick Warmup",
        image_count=10,
        duration_seconds=30
    )
    
    assert preset.name == "Quick Warmup"
    assert preset.image_count == 10