from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    # Optional: prevent duplicate names under same parent
    query = select(Category).where(
        Category.name == category.name,
        Category.parent_id == category.parent_id
    )
    result = await db.execute(query)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists in this folder"
        )

    new_category = Category(**category.dict())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category

@router.get("/", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category).order_by(Category.name)
    )
    return result.scalars().all()