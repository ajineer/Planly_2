# Tests

## user routes

- signup users
- login users
- check user session (should return sent and received invites)

## data routes

- make calendar(s)
- get calendars(s) and their event(s)/task(s)
- patch calendar name or description
- delete calendar and all theier events and tasks (one api call)
- add events/tasks
- patch events/tasks
- delete individual events/tasks

## Invites and collaborations

- send invite
- other user accepts and interacts with shared calendar (either read only or write only)
- create collaboration and set its' permissions
- guest user can read only calendar data
- gueet user can write data to calendar (name, description, events and tasks)
- modify permissions (demote user to read only and try full CRUD on calendar, events and tasks)
- revoke access completely from user (i.e. delete collaboration)
