from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from model import Image, SessionPreset
from schemas import ImageOut, SessionPresetOut, SessionPresetCreate
from images import sync_local_images, get_random_images, save_uploaded_image, ALLOWED_EXTENSIONS

# Add default session presets if they don't exist
def seed_default_presets(db: Session):
    defaults = [
        ("Quick Warmup", 10, 30),
        ("Standard Practice", 20, 60),
        ("Long Study", 5, 300),
    ]
    for name, count, duration in defaults:
        if not db.query(SessionPreset).filter_by(name=name).first():
            db.add(SessionPreset(name=name, image_count=count, duration_seconds=duration))
    db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and sync images
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    sync_local_images(db)
    seed_default_presets(db)
    db.close()
    yield
    # Shutdown: nothing to clean up

# Start up our FastAPI app with lifespan management
app = FastAPI(title="Tybee API", lifespan=lifespan)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to list all images
@app.get("/images", response_model=list[ImageOut])
def list_images(db: Session = Depends(get_db)):
    return db.query(Image).all()

# Endpoint to get random images for a session
@app.get("/images/random", response_model=list[ImageOut])
def random_images(count: int = 10, db: Session = Depends(get_db)):
    return get_random_images(db, count)

# Endpoint to serve an image file
@app.get("/images/{image_id}/file")
def get_image_file(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter_by(id=image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image.filepath)

# Endpoint to upload a new image
@app.post("/images/upload", response_model=ImageOut)
async def upload_image(file: UploadFile, db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type not allowed. Use: {ALLOWED_EXTENSIONS}")
    
    return await save_uploaded_image(file, db)

# List session presets
@app.get("/presets", response_model=list[SessionPresetOut])
def list_presets(db: Session = Depends(get_db)):
    return db.query(SessionPreset).all()

# Create a new session preset
@app.post("/presets", response_model=SessionPresetOut)
def create_preset(preset: SessionPresetCreate, db: Session = Depends(get_db)):
    db_preset = SessionPreset(**preset.model_dump())
    db.add(db_preset)
    db.commit()
    db.refresh(db_preset)
    return db_preset