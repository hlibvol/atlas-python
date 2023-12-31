from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.db.lessons.models import Lesson
from app.db.core import delete_item


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        name=course.name,
        description=course.description,
        duration=course.duration,
        enroll_required=course.enroll_required,
        passing_percentage=course.passing_percentage,
        created_by=course.created_by,
    )
    db.add(db_course)
    db.commit()

    if course.items is not None and len(course.items) > 0:
        db_course_item = [
            models.CourseItems(
                course_id=db_course.id,
                item_type=items.item_type,
                item_title=items.item_title,
                item_id=items.item_id,
                item_order=items.item_order,
            )
            for items in course.items
        ]
        db.add_all(db_course_item)
        db.commit()

    db.refresh(db_course)
    return db_course


def edit_course(
    db: Session, course_id: int, course: schemas.CourseEdit
) -> schemas.Course:
    course_item = get_course_item(db, course_id)
    db_course = (
        db.query(models.Course).filter(models.Course.id == course_id).first()
    )
    if not db_course:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Course not found"
        )
    update_data = course.dict(exclude_unset=True)

    items_to_delete = [
        db_item.id
        for db_item in db_course.items
        if db_item.id not in [item.id for item in course.items]
    ]
    delete_extra_course_items(db, items_to_delete)

    for key, value in update_data.items():
        if key == "items":
            for item in value:
                if "id" in item:
                    course_item = (
                        db.query(models.CourseItems)
                        .filter(models.CourseItems.id == item["id"])
                        .first()
                    )
                    if course_item:
                        setattr(course_item, "item_order", item["item_order"])
                else:
                    item_id = 0
                    if item["item_type"] == "LESSON":
                        resp = get_lesson_by_name_create_if_none(
                            db, item["item_title"]
                        )
                        item_id = resp.id
                    db_course_items = models.CourseItems(
                        course_id=db_course.id,
                        item_type=item["item_type"],
                        item_title=item["item_title"],
                        item_id=item_id,
                        item_order=item["item_order"],
                    )
                    db.add(db_course_items)
                    db.commit()

        else:
            setattr(db_course, key, value)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course_item(db: Session, course_id: int):
    course_item = get_course_item(db, course_id)
    if course_item:
        for value in course_item:
            db.delete(value)
    db.commit()
    return course_item


def get_course_item(db: Session, course_id: int):
    course = (
        db.query(models.CourseItems)
        .filter(models.CourseItems.course_id == course_id)
        .all()
    )
    if course:
        return course


def get_course_item_by_id(db: Session, id: int):
    course = db.query(models.CourseItems).get(id)
    if course:
        return course


def delete_extra_course_items(db: Session, item_to_delete: any):
    course_item = (
        db.query(models.CourseItems)
        .filter(models.CourseItems.id.in_(item_to_delete))
        .all()
    )
    # db.delete(course)
    for item_row in course_item:
        db.delete(item_row)
        if item_row.item_type == "LESSON":
            delete_item(db, Lesson, item_row.item_id)
    db.commit()
    return True


def get_lesson_by_name_create_if_none(db: Session, name: str):
    lesson = db.query(Lesson).filter(Lesson.name == name).first()
    if not lesson:
        db_lesson = Lesson(name=name, is_template=False)
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        return db_lesson
    return lesson
