import React, { useEffect, useState } from 'react'
import { useCalendarContext, useTaskContext } from '../hooks/useDataContext'
import { useAuthContext } from '../hooks/useAuthContext'
import { createTask, deleteTask, fetchTasks, patchTask } from '../apiRoutes/TaskRoutes'

const TaskApiTest = () => {
  
    const {tasks, dispatch} = useTaskContext()
    const {calendars} = useCalendarContext()
    const {user} = useAuthContext()
    const [error, setError] = useState(null)
    const [message, setMessage] = useState(null)
  

    const handleGetTasks = async () => {
        setError(null)
        setMessage(null)
        const response = await fetchTasks(user, {start: "2024-07-01", end: "2024-07-31"})
        
        const json = await response.json()
        
        if (!response.ok){
            setError(json?.error || "error occurred")
        }
    
        if (response.ok){
            setMessage(json?.message)
            dispatch({type: "SET_TASKS", payload: json})
        }
    }
    const handleCreateTask = async () => {
        setError(null)
        setMessage(null)
        const response = await createTask(user, {title: "Task1.1", description: "Task1.1", date: "2024-07-21", calendar_id: calendars[0].id, status: 0,})
        
        const json = await response.json()
        
        if (!response.ok){
            setError(json?.error || "error occurred")
        }
    
        if (response.ok){
            setMessage(json?.message)
            dispatch({type: "CREATE_TASKS", payload: json})
        }
    }
    const handlePatchTask = async () => {
        setError(null)
        setMessage(null)
        const response = await patchTask(user, {...tasks[0], status: 1})
        const json = await response.json()

        if (!response.ok){
            setError(json?.error || "error occurred")
        }
    
        if (response.ok){
            setMessage(json?.message)
            dispatch({type: "UPDATE_TASKS", payload: json})
        }

    }
    const handleDeleteTask = async () => {
        setError(null)
        setMessage(null)
        const response = await deleteTask(user, tasks[0])
        
        const json = await response.json()
        
        if (!response.ok){
            setError(json?.error || "error occurred")
        }
    
        if (response.ok){
            setMessage(json?.message)
            dispatch({type: "DELETE_TASKS", payload: tasks[0]})
        }
    }


    useEffect(() => {
        console.log(tasks)
    },[tasks, dispatch])

    return (
        <div>
            <button onClick={() => handleGetTasks()}>Get Tasks</button>
            <button onClick={() => handleCreateTask()}>Create Tasks</button>
            <button onClick={() => handlePatchTask()}>Patch Task</button>
            <button onClick={() => handleDeleteTask()}>Delete Task</button>
            {message && <div>{message}</div>}
            {error && <div>{error}</div>}
        </div>
  )
}

export default TaskApiTest