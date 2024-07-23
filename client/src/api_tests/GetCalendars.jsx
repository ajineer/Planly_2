import React, { useEffect, useState } from 'react'
import { useAuthContext } from '../hooks/useAuthContext'
import { useCalendarContext } from '../hooks/useDataContext/'
import { createCalendar, deleteCalendar, fetchCalendars, patchCalendar } from '../apiRoutes/CalendarRoutes'
import { useTaskContext } from '../hooks/useDataContext'

const GetCalendars = () => {
  
  const {user} = useAuthContext()
  const {calendars, dispatch} = useCalendarContext()
  const {tasks, dispatch: taskDispatch} = useTaskContext()
  const [isLoading, setIsLoading] = useState(null)
  const [error, setError] = useState(null)

  const handleGetCalendars = async () => {
    
    const response = await fetchCalendars(user) 

    const json = await response.json()

    if(!response.ok || !json){
        setIsLoading(false)
        setError(json?.error || 'error occured')
    }
    if(response.ok){
        // console.log("json: ", json)
        dispatch({type: 'SET_CALENDARS', payload:json})
    }
  }

  const handlePatchCalendar = async (calendar) => {
        const response = await patchCalendar(user, calendar)
        const json = await response.json()

        if(!response.ok || !json){
            setIsLoading(false)
            setError(json?.error || 'error occured')
        }
        if(response.ok){
            // console.log("json: ", json)
            dispatch({type: 'UPDATE_CALENDARS', payload:json})
        }
    }
  const handleCreateCalendar = async (calendar) => {
        const response = await createCalendar(user, calendar)
        const json = await response.json()

        if(!response.ok || !json){
            setIsLoading(false)
            setError(json?.error || 'error occured')
        }
        if(response.ok){
            // console.log("json: ", json)
            dispatch({type: 'CREATE_CALENDARS', payload:json})
        }
    }

  const handleDeleteCalendar = async (calendar) => {
    const response = await deleteCalendar(user, calendar)
    const json = await response.json()

    if(!response.ok || !json){
        setIsLoading(false)
        setError(json?.error || 'error occured')
    }
    if(response.ok){
        // console.log("json: ", json)
        dispatch({type: 'DELETE_CALENDARS', payload:calendar})
    }

  }



  useEffect(() => {
    console.log(calendars)
  }, [calendars, dispatch])

  return (
    <div>
        <button onClick={() => handleGetCalendars()}>
            Get Calendars
        </button>
        <button onClick={() => handlePatchCalendar({
            'id': '0cf5093c-d748-4d9b-b94c-f6141b8cd1a6',
            'name': 'Calendar 1.1',
            'description': 'Calendar 1.1'
            })
        }>
            Patch Calendar
        </button>
        <button onClick={() => handleDeleteCalendar({
            'id': '0cf5093c-d748-4d9b-b94c-f6141b8cd1a6',
            'name': 'Calendar 1.1',
            'description': 'Calendar 1.1'
        })}>
            Delete Calendar
        </button>
        <button onClick={() => handleCreateCalendar({
            'name':'Calendar 1.1',
            'description':'Calendar 1.1',
        })}>
            Create Calendar
        </button>

    </div>
  )
}

export default GetCalendars