export const fetchTasks = async (user, body) => {
  const response = await fetch("/api/tasks/query", {
    method: "POST",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  return response;
};

export const patchTask = async (user, task) => {
  const response = await fetch("/api/tasks/patch", {
    method: "PATCH",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(task),
  });

  return response;
};

export const deleteTask = async (user, task) => {
  const response = await fetch(`/api/tasks/delete/${task.id}`, {
    method: "DELETE",
    headers: {
      Authorization: `bearer ${user.token}`,
    },
  });

  return response;
};

export const createTask = async (user, task) => {
  console.log(task);
  const response = await fetch("/api/tasks/create", {
    method: "POST",
    headers: {
      Authorization: `bearer ${user.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(task),
  });

  return response;
};
