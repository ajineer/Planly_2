from ..config import api
from .taskRoutes import Tasks, TasksById

# task routes
api.add_resource(Tasks, "/tasks")
api.add_resource(TasksById, "/task/<int:task_id>")
