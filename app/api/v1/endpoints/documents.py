from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pathlib import Path
import shutil
import uuid

from app.core.dependencies import get_db
from app.models.document import Document
from app.schemas.document import DocumentListResponse

router = APIRouter()

# Storage directory
STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)


# ===============================
# LIST DOCUMENTS
# ===============================
@router.get("/", response_model=list[DocumentListResponse])
async def list_documents(
    category_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Document).options(selectinload(Document.category))

    if category_id is not None:
        query = query.where(Document.category_id == category_id)

    result = await db.execute(query.order_by(Document.uploaded_at.desc()))
    docs = result.scalars().all()

    return [
        DocumentListResponse(
            id=doc.id,
            name=doc.name,
            description=doc.description,
            filename=doc.filename,
            category_id=doc.category_id,
            category_name=doc.category.name if doc.category else None,
            uploaded_at=doc.uploaded_at,
        )
        for doc in docs
    ]


# ===============================
# UPLOAD DOCUMENT
# ===============================
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    name: str = Form(...),
    description: str | None = Form(None),
    category_id: int | None = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # Validate name
    if not name.strip():
        raise HTTPException(status_code=400, detail="Document name is required")

    # Create unique filename to avoid overwrite
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = STORAGE_DIR / unique_filename

    # Save file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata
    document = Document(
        name=name.strip(),
        description=description,
        filename=file.filename,   # original filename
        file_path=str(file_path), # stored path
        category_id=category_id,
    )

    db.add(document)
    await db.commit()
    await db.refresh(document)

    return {
        "id": document.id,
        "name": document.name,
        "message": "Document uploaded successfully"
    }