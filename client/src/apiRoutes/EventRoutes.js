export const fetchEvents = async (user, body) => {
  const response = await fetch("/api/events/query", {
    method: "POST",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  return response;
};

export const patchEvent = async (user, event) => {
  const response = await fetch("/api/events/patch", {
    method: "PATCH",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(event),
  });

  return response;
};

export const deleteEvent = async (user, event) => {
  const response = await fetch(`/api/events/delete/${event.id}`, {
    method: "DELETE",
    headers: {
      Authorization: `bearer ${user.token}`,
    },
  });

  return response;
};

export const createEvent = async (user, event) => {
  const response = await fetch("/api/events/create", {
    method: "POST",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(event),
  });

  return response;
};
