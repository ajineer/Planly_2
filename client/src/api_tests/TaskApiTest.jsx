import React, { useEffect, useState } from 'react'
import { useAuthContext } from '../hooks/useAuthContext'
import { useCalendarContext, useTaskContext } from '../hooks/useDataContext'
import { createTasksRoute, deleteTasksRoute, getTasksRoute, patchTasksRoute } from '../apiRoutes/TaskRoutes'
import { fetchCalendar } from '../apiRoutes/CalendarRoutes'

const TaskApiTest = () => {

  const {user} = useAuthContext()
  const {tasks, dispatch: taskDispatch} = useTaskContext()
  const {calendars, dispatch: calendarDispatch} = useCalendarContext()
  const new_task_body = {
    'calendar_string_id': "0e8fa0e5-0ba7-4c62-b254-24566a6971ed",
    'date': "now",
    'description': "Task1.1",
    'status': "incomplete",
    'title': "Task1.1",
  }
  const patch_task_body = {...calendars[0]?.tasks[0], status: 'complete'}

  const handleCreateTasks = async (task_body) => {
    const taskResponse = await createTasksRoute(user, task_body)
    const calendarResponse = await fetchCalendar(user, task_body.calendar_string_id)
    const calendar = await calendarResponse.json()
    if(!taskResponse.ok || !calendarResponse.ok || !calendar){
        alert(new_task?.error, calendar?.error)
    }
    if(taskResponse.ok && calendarResponse.ok){
        calendarDispatch({type: 'UPDATE_CALENDARS', payload:calendar})
    }

  }

  const handlePatchTask = async (task) => {
    const response = await patchTasksRoute(user, task)
    const CalendarResponse = await fetchCalendar(user, task.calendar_id)
    
    const calendar = await CalendarResponse.json()
    const json = await response.json()

    if(!response.ok || !json || !CalendarResponse.ok || !calendar){
      alert(json?.error, calendar?.error)
    }
    if(response.ok){
      calendar.tasks = calendar.tasks.map(t => t.id == json.id ? json : t)
      calendarDispatch({type: 'UPDATE_CALENDARS', payload: calendar})
    }
  }

  const handleDeleteTask = async (task) => {
    console.log(task)
    const taskResponse = await deleteTasksRoute(user, task)
    const calendarResponse = await fetchCalendar(user, task.calendar_id)

    const calendar = await calendarResponse.json()

    if(!taskResponse.ok || !calendarResponse.ok || !calendar){
        alert(response.status, calendarResponse.status)
      }
    if(taskResponse.ok && calendarResponse.ok){
        calendar.tasks.filter(t => t.id !== task.id)
        calendarDispatch({type:'UPDATE_CALENDARS', payload:calendar})
      }
  }
  
  useEffect(() => {
    console.log(calendars.tasks)
  },[calendars, calendarDispatch])

  return (
    <div>
        <button onClick={() => handleCreateTasks(new_task_body)}>
            Create Task
        </button>
        <button onClick={() => handlePatchTask(patch_task_body)}>
            Patch Task
        </button>
        <button onClick={() => handleDeleteTask(calendars[0]?.tasks[0])}>
            Delete Task
        </button>
    </div>
  )
}

export default TaskApiTest