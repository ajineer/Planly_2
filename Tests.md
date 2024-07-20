# Tests

## user routes

[x] signup users
[x] login users
[x] check user session (should return sent and received invites)

## data routes

[x] make calendar(s)
[x] get calendars(s) and their event(s)/task(s)
[x] patch calendar name or description
[x] delete calendar and all their events and tasks (one api call)
[x] add events/tasks
[x] patch events/tasks
[x] delete individual events/tasks
[x] collaboration is created when invite is accepted (patch to invite and post to collaborations)
[x] owner can patch collaboration and adjust permissions for the guest

## Invites and collaborations

[x] send invite
[x] other user accepts/declines invite and
[x] guest user can read only calendar data
[x] guest user can patch events as a guest
[x] guest user can post events as a guest
[x] guest user can patch tasks as a guest
[x] guest user can post tasks as a guest
[x] revoke access completely from user (i.e. delete collaboration)
