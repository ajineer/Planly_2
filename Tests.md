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
[x] collaboration is created when invite is accepted (patch to invite and post to collaborations)
[ ] owner can patch collaboration and adjust permissions for the guest

## Invites and collaborations

[x] send invite
[x] other user accepts/declines invite and
[ ] guest user can read only calendar data
[x] guest user can patch events as a guest
[ ] guest user can post events as a guest
[ ] guest user can patch tasks as a guest
[ ] guest user can post tasks as a guest
[ ] owner can modify permissions (demote user to read only and try full CRUD on calendar, events and tasks)
[ ] revoke access completely from user (i.e. delete collaboration)
