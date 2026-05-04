from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Give frontend just enough info to request the image file
class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    source: str
    uploaded_at: datetime

# Return preset info
class SessionPresetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image_count: int
    duration_seconds: int

# Create preset request body
class SessionPresetCreate(BaseModel):
    name: str
    image_count: int
    duration_seconds: int