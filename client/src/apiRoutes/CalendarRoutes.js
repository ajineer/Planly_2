export const fetchCalendars = async (user) => {
  const response = await fetch(`/api/calendars`, {
    headers: {
      Authorization: `bearer ${user.token}`,
    },
  });

  return response;
};

export const patchCalendar = async (user, calendar) => {
  const response = await fetch(`/api/calendars/patch`, {
    method: "PATCH",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(calendar),
  });

  return response;
};

export const deleteCalendar = async (user, calendar) => {
  const response = await fetch(`/api/calendars/delete/${calendar.id}`, {
    method: "DELETE",
    headers: {
      Authorization: `bearer ${user.token}`,
    },
  });

  return response;
};

export const createCalendar = async (user, calendar) => {
  const response = await fetch(`/api/calendars`, {
    method: "POST",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(calendar),
  });

  return response;
};
