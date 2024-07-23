export const getTasksRoute = async (user) => {
  const response = await fetch("/api/calendars", {
    headers: {
      Authorization: `bearer ${user.token}`,
    },
  });

  return response;
};
export const createTasksRoute = async (user, task) => {
  const response = await fetch("/api/tasks", {
    method: "POST",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(task),
  });

  return response;
};
export const patchTasksRoute = async (user, task) => {
  const response = await fetch(`/api/tasks/${task.id}`, {
    method: "PATCH",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(task),
  });

  return response;
};
export const deleteTasksRoute = async (user, task) => {
  const response = await fetch(`/api/tasks/${task.id}`, {
    method: "DELETE",
    headers: {
      Authorization: `bearer ${user.token}`,
    },
  });

  return response;
};
