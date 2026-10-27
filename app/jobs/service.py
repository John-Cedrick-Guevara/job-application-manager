from sqlalchemy import select
from sqlalchemy.orm import Session
from app.jobs import schema
from app.jobs import model 

from datetime import datetime, timezone

def create_job(db: Session, job: schema.JobCreate) -> model.Job:
    db_job = model.Job(**job.model_dump())
    

    if not job.posted_at:
        db_job.posted_at = datetime.now(timezone.utc)

    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    return db_job

def get_job(db: Session, job_id: int) -> model.Job | None:
    return db.get(model.Job, job_id)

def get_jobs(db: Session, skip: int, limit: int) -> list[model.Job]:
    return db.scalars(select(model.Job).offset(skip).limit(limit)).all()

def update_job(db: Session, job_id: int, job: schema.JobUpdate) -> model.Job | None:
    db_job = db.get(model.Job, job_id)
    if not db_job:
        return None

    # Update the fields of the db_job with the values from the job object
    for key, value in job.model_dump(exclude_unset=True).items():
        setattr(db_job, key, value)
    
    db.commit()
    db.refresh(db_job)
    
    return db_job

def delete_job(db: Session, job_id: int) -> bool:
    db_job = db.get(model.Job, job_id)
    if not db_job:
        return False

    db.delete(db_job)
    db.commit()
    
    return True