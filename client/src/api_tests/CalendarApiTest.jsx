import React, { useEffect, useState } from 'react'
import { useCalendarContext } from '../hooks/useDataContext'
import { createCalendar, deleteCalendar, fetchCalendars, patchCalendar } from '../apiRoutes/CalendarRoutes'
import { useAuthContext } from '../hooks/useAuthContext'

const CalendarApiTest = () => {
  
  const {calendars, dispatch} = useCalendarContext()
  const [error, setError] = useState(null)
  const [message, setMessage] = useState(null)
  const [patchedCalendar, setPatchedCalendar] = useState({})
  const { user } = useAuthContext()
  
  const handleGetCalendars = async () => {
    setMessage(null)
    setError(null)
    const response = await fetchCalendars(user)
    const json = await response.json()

    if (!response.ok){
        setError(json?.error || "error occured")
    }

    if (response.ok){
        dispatch({type: "SET_CALENDARS", payload: json})
    }
  }

  const handleCreateCalendar = async () => {
    setMessage(null)
    setError(null)
    const response = await createCalendar(user, {"name": "Calendar1.1", "description": "Calendar1.1"})

    const json = await response.json()

    if (!response.ok){
        setError(json?.error || "error occured")
    }

    if (response.ok){
        dispatch({type: "CREATE_CALENDARS", payload: json})
    }
  }

  const handleDeleteCalendar = async () => {
    setMessage(null)
    setError(null)
    const response = await deleteCalendar(user, calendars[0])
    
    const json = await response.json()

    if (!response.ok){
        setError(json?.error || "error occurred")
    }

    if (response.ok){
        setMessage(json?.message)
        dispatch({type: "DELETE_CALENDARS", payload: calendars[0]})
    }
  }

  const handlePatchCalendar = async () => {
    setMessage(null)
    setError(null)
    const response = await patchCalendar(user, patchedCalendar)

    const json = await response.json()

    if (!response.ok){
        setError(json?.error || "error occurred")
    }

    if (response.ok){
        setMessage(json?.message)
        dispatch({type: "UPDATE_CALENDARS", payload: json})
    }
  }

  useEffect(() => {
    console.log(calendars)
  }, [calendars, dispatch])

  return (
    <div>
        <button onClick={() => handleGetCalendars()}>Get Calendars</button>
        <button onClick={() => handleCreateCalendar()}>Create Calendar</button>
        <button onClick={()=> handleDeleteCalendar()}>Delete Calendar</button>
        <button onClick={() => {setPatchedCalendar({...calendars[0], description: "calendar1.1"}), handlePatchCalendar()}}>Patch Calendar</button>
        {error && <div>{error}</div>}
        {message && <div>{message}</div>}
    </div>
  )
}

export default CalendarApiTest