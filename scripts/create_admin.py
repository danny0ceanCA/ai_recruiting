"""Bootstrap admin user."""
import argparse
from sqlalchemy.orm import Session

from app.database import SessionLocal, init
from app.models import models


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--school", required=True)
    args = parser.parse_args()

    init()
    db: Session = SessionLocal()
    admin = models.Student(
        name=args.name,
        school_id=0,
        background=f"Admin for {args.school}",
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"Created admin id={admin.id}")

if __name__ == "__main__":
    main()
