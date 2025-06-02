"""Bulk upload students from CSV."""
import csv
import argparse
from sqlalchemy.orm import Session

from app.database import SessionLocal, init
from app.models import models


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="CSV file with student data")
    args = parser.parse_args()

    init()
    db: Session = SessionLocal()
    with open(args.csv_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = models.Student(
                name=row.get("name", ""),
                school_id=int(row.get("school_id", 0)),
                background=row.get("background"),
                education=row.get("education"),
                experience=row.get("experience"),
                qualities=row.get("qualities"),
            )
            db.add(student)
        db.commit()
    print("Bulk upload complete")

if __name__ == "__main__":
    main()
