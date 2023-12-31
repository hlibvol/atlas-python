from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from . import models, schemas
from app.db.users.crud import get_user
from app.core import security
from app.db.jobs.models import Job
from app.db.use_cases.models import UseCase
from app.db.screens.models import Screen
from sqlalchemy.orm.attributes import flag_modified

__all__ = ("delete_all_job_mappings", "update_job_mappings")


def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()


def validate_user_and_job(db: Session, job_id, user_id, mode):
    user = get_user(db, user_id)
    if mode == schemas.ExtensionMode.DESIGNER and not user.is_designer:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="User has no designer access."
        )

    job = get_job(db, job_id)
    if job.is_locked:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Job is locked by another user."
        )

    return job


def delete_all_job_mappings(db: Session, job_id: int, model=None):
    # Remove role reference from other models
    affected_models = [Screen, UseCase] if not model else [model]

    for model in affected_models:
        items = db.query(model).filter(model.job_ids.any(job_id)).all()
        for item in items:
            item.job_ids.remove(job_id)
            flag_modified(item, "job_ids")
            db.merge(item)
            db.flush()
            db.commit()


def update_job_mappings(db: Session, job_id, job: Job):
    if job.screen_ids:
        delete_all_job_mappings(db, job_id, Screen)
        screens = db.query(Screen).filter(Screen.id.in_(job.screen_ids)).all()
        for screen in screens:
            screen.job_ids.append(job_id)
            flag_modified(screen, "job_ids")
            db.merge(screen)
            db.flush()
            db.commit()

    if job.use_case_ids:
        delete_all_job_mappings(db, job_id, UseCase)
        use_cases = (
            db.query(UseCase).filter(UseCase.id.in_(job.use_case_ids)).all()
        )
        for use_case in use_cases:
            use_case.job_ids.append(job_id)
            flag_modified(use_case, "job_ids")
            db.merge(use_case)
            db.flush()
            db.commit()


# def delete_job_mapping(db: Session, job_id: int):
#     # delete job mapping in use case
#     affected_use_cases = (
#         db.query(UseCase).filter(UseCase.job_ids.any(job_id)).all()
#     )
#     for use_case in affected_use_cases:
#         use_case.job_ids.remove(job_id)
#         flag_modified(use_case, "job_ids")
#         db.merge(use_case)
#         db.flush()
#         db.commit()
