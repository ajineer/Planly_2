import React, { useEffect, useState } from 'react'
import { useCalendarContext, useEventContext } from '../hooks/useDataContext'
import { createEvent, deleteEvent, fetchEvents, patchEvent } from '../apiRoutes/EventRoutes'
import { useAuthContext } from '../hooks/useAuthContext'

const EventApiTest = () => {

    const {events, dispatch} = useEventContext()
    const {calendars} = useCalendarContext()
    const {user} = useAuthContext()
    const [error, setError] = useState(null)
    const [message, setMessage] = useState(null)

    const handleGetEvents = async () => {
        setError(null)
        setMessage(null)
        const response = await fetchEvents(user, {start: "2024-07-01", end: "2024-07-31"})
        
        const json = await response.json()
        
        if (!response.ok){
            setError(json?.error || "error occurred")
        }
    
        if (response.ok){
            setMessage(json?.message)
            dispatch({type: "SET_EVENTS", payload: json})
        }
    }
    const handleCreateEvent = async () => {
        setError(null)
        setMessage(null)
        const response = await createEvent(user, {name: "Event1.1", description: "Event1.1", start: "2024-07-13", end: "2024-07-21", calendar_string_id: calendars[0].id})
        
        const json = await response.json()
        
        if (!response.ok){
            setError(json?.error || "error occurred")
        }
    
        if (response.ok){
            setMessage(json?.message)
            dispatch({type: "CREATE_EVENTS", payload: json})
        }
    }
    const handlePatchEvent = async () => {
        setError(null)
        setMessage(null)
        const response = await patchEvent(user, {...events[0], start: "2024-08-03", end: "2024-08-24"})
        const json = await response.json()

        if (!response.ok){
            setError(json?.error || "error occurred")
        }
    
        if (response.ok){
            setMessage(json?.message)
            dispatch({type: "UPDATE_EVENTS", payload: json})
        }

    }
    const handleDeleteEvent = async () => {
        setError(null)
        setMessage(null)
        const response = await deleteEvent(user, events[0])
        
        const json = await response.json()
        
        if (!response.ok){
            setError(json?.error || "error occurred")
        }
    
        if (response.ok){
            setMessage(json?.message)
            dispatch({type: "DELETE_EVENTS", payload: events[0]})
        }
    }

    useEffect(() => {
        console.log(events)
    },[events, dispatch]) 

  return (
    <div>
        <button onClick={() => handleGetEvents()}>Get Events</button>
        <button onClick={() => handleCreateEvent()}>Create Event</button>
        <button onClick={() => handlePatchEvent()}>Patch Event</button>
        <button onClick={() => handleDeleteEvent()}>Delete Event</button>
        {message && <div>{message}</div>}
        {error && <div>{error}</div>}
    </div>
  )
}

export default EventApiTest