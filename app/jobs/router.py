from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.jobs import schema
from app.jobs import service


router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.post("/", response_model=schema.JobCreate, status_code=status.HTTP_201_CREATED)
def create_job(job: schema.JobCreate, db: Session = Depends(get_db)):
    return service.create_job(db, job)

@router.get("/{job_id}", response_model=schema.JobRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    db_job = service.get_job(db, job_id)
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return db_job

@router.get("/", response_model=list[schema.JobRead])
def get_jobs(skip: int, limit: int, db: Session = Depends(get_db)):
    return service.get_jobs(db, skip=skip, limit=limit)

@router.put("/{job_id}", response_model=schema.JobRead)
def update_job(job_id: int, job: schema.JobUpdate, db: Session = Depends(get_db)):
    db_job = service.update_job(db, job_id, job)
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return db_job

@router.delete("/{job_id}", response_model=schema.JobRead)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = service.get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    service.delete_job(db, job_id)
    return job