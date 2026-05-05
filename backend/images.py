import os
import random
from pathlib import Path
from sqlalchemy.orm import Session

from model import Image

REFERENCE_DIR = Path(__file__).parent / "reference-images"
UPLOAD_DIR = REFERENCE_DIR / "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Ensure are reference and upload directories exist
def ensure_dirs():
    REFERENCE_DIR.mkdir(exist_ok=True)
    UPLOAD_DIR.mkdir(exist_ok=True)


# Scan reference-images folder and add new images to database
def sync_local_images(db: Session):
    ensure_dirs()
    
    # Get paths already in database
    existing_paths = {img.filepath for img in db.query(Image).all()}
    
    # Scan folder for image files
    for filepath in REFERENCE_DIR.iterdir():
        if filepath.is_file() and filepath.suffix.lower() in ALLOWED_EXTENSIONS:
            str_path = str(filepath)
            if str_path not in existing_paths:
                image = Image(
                    filename=filepath.name,
                    filepath=str_path,
                    source="local"
                )
                db.add(image)
    
    db.commit()

# Get random images for a session
def get_random_images(db: Session, count: int) -> list[Image]:
    all_images = db.query(Image).all()
    if not all_images:
        return []
    return random.sample(all_images, min(count, len(all_images)))

# Save an uploaded image, ensuring no filename conflicts, and add it to the database
async def save_uploaded_image(file, db: Session) -> Image:
    ensure_dirs()
    
    filepath = UPLOAD_DIR / file.filename
    
    # Handle duplicate filenames
    counter = 1
    while filepath.exists():
        stem = Path(file.filename).stem
        suffix = Path(file.filename).suffix
        filepath = UPLOAD_DIR / f"{stem}_{counter}{suffix}"
        counter += 1
    
    # Save file to disk
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Add to database
    image = Image(
        filename=filepath.name,
        filepath=str(filepath),
        source="upload"
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    
    return image