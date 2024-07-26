from models import User, Calendar, Invite, Event, Task, Collaboration
from config import db, app
from datetime import datetime
from uuid import UUID

if __name__ == "__main__":

    with app.app_context():
        while True:
            choice = input(
                """
                1. drop all tables
                2. create all tables
                3. delete users
                4. delete calendars
                5. delete events
                6. delete tasks
                7. delete collaborations
                8. delete invites
                9. generate calendar
                10. generate events
                11. generate tasks
            """
            )
            if choice == "1":
                db.drop_all()
            elif choice == "2":
                db.create_all()
            elif choice == "3":
                User.query.delete()
                db.session.commit()
            elif choice == "4":
                print("deleting calendars")
                Calendar.query.delete()
                db.session.commit()
            elif choice == "5":
                Event.query.delete()
                db.session.commit()
            elif choice == "6":
                Task.query.delete()
                db.session.commit()
            elif choice == "7":
                Collaboration.query.delete()
                db.session.commit()
            elif choice == "8":
                Invite.query.delete()
                db.session.commit()
            elif choice == "9":
                calendar = Calendar(
                    user_id=UUID("f23735c775554d95b1910342fd6c674a"),
                    name="Calendar1.1",
                    description="Calendar1.1",
                )
                db.session.add(calendar)
                db.session.commit()
            elif choice == "10":
                calendar = Calendar.query.filter(
                    Calendar.user_id == UUID("f23735c775554d95b1910342fd6c674a")
                ).first()
                events = []
                for i in range(3):
                    name = f"Event 1.{i}"
                    start = datetime(2024, 7, i + 1)
                    end = datetime(2024, 7, i + 2)
                    new_event = Event(
                        calendar_id=calendar.id,
                        name=name,
                        description=name,
                        start=start,
                        end=end,
                    )
                    events.append(new_event)

                for i in range(3):
                    names = f"Event 1.{i}"
                    start = datetime(2024, 8, i + 4)
                    end = datetime(2024, 8, i + 5)
                    new_event = Event(
                        calendar_id=calendar.id,
                        name=name,
                        description=name,
                        start=start,
                        end=end,
                    )
                    events.append(new_event)

                db.session.add_all(events)
                db.session.commit()

            elif choice == "11":
                calendar = Calendar.query.filter(
                    Calendar.user_id == UUID("f23735c775554d95b1910342fd6c674a")
                ).first()
                tasks = []
                for i in range(3):
                    title = f"Task 1.{i+3}"
                    date = datetime(2024, 8, i + 3)
                    new_task = Task(
                        calendar_id=calendar.id,
                        title=title,
                        description=title,
                        date=date,
                        status="incomplete",
                    )
                    tasks.append(new_task)

                db.session.add_all(tasks)
                db.session.commit()

            elif choice == "":
                break
