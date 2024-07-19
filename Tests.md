# Tests

## user routes

[x] signup users
[x] login users
[x] check user session (should return sent and received invites)

## data routes

[x] make calendar(s)
[x] get calendars(s) and their event(s)/task(s)
[x] patch calendar name or description
[x] delete calendar and all theier events and tasks (one api call)
[x] add events/tasks
[x] patch events/tasks
[x] delete individual events/tasks

## Invites and collaborations

[x] send invite
[x] other user accepts/declines invtie and
[ ] (skip this one, guests cannot do anything to the calendar itself) guest user interacts with shared calendar (patch title or description)
[ ] guest user can read only calendar data
[ ] gueet user can write data (with right permissions) to calendar (events and tasks)
[ ] owner can modify permissions (demote user to read only and try full CRUD on calendar, events and tasks)
[ ] revoke access completely from user (i.e. delete collaboration)
