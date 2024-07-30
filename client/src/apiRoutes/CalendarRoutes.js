export const fetchCalendars = async (user) => {
  if (!user || !user.token) {
    return new Response(
      JSON.stringify({ error: "User is not authorized to use this route" }),
      {
        status: 401,
        statusText: "Not Authorized",
        ok: false,
      }
    );
  }
  const response = await fetch(`/api/calendars`, {
    headers: {
      Authorization: `bearer ${user.token}`,
    },
  });

  return response;
};

export const patchCalendar = async (user, calendar) => {
  if (!user || !user.token) {
    return new Response(
      JSON.stringify({ error: "User is not authorized to use this route" }),
      {
        status: 401,
        statusText: "Not Authorized",
        ok: false,
      }
    );
  }
  if (!calendar || !calendar.id) {
    return new Response(
      JSON.stringify({ error: "Must provide a calendar object to patch" }),
      {
        status: 400,
        statusText: "Bad request",
        ok: false,
      }
    );
  }
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
  if (!user || !user.token) {
    return new Response(
      JSON.stringify({ error: "User is not authorized to use this route" }),
      {
        status: 401,
        statusText: "Not Authorized",
        ok: false,
      }
    );
  }
  if (!calendar) {
    return new Response(
      JSON.stringify({ error: "Must provide a calendar object to delete" }),
      {
        status: 400,
        statusText: "Bad request",
        ok: false,
      }
    );
  }
  const response = await fetch(`/api/calendars/delete/${calendar.id}`, {
    method: "DELETE",
    headers: {
      Authorization: `bearer ${user.token}`,
    },
  });

  return response;
};

export const createCalendar = async (user, calendar) => {
  if (!user || !user.token) {
    return new Response(
      JSON.stringify({ error: "User is not authorized to use this route" }),
      {
        status: 401,
        statusText: "Not Authorized",
        ok: false,
      }
    );
  }
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
