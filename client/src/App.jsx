import React, { useEffect, useState } from 'react'
import AuthTests from './api_tests/AuthTests'
import CalendarApiTest from './api_tests/CalendarApiTest'
import EventApiTest from './api_tests/EventApiTest'
import TaskApiTest from './api_tests/TaskApiTest'
import { useAuthContext } from './hooks/useAuthContext'
import './App.css'
import { useLogout } from './hooks/useLogout'

function App() {

  const {user, dispatch} = useAuthContext()
  const {logout} = useLogout()
  const {error, setError} = useState()

  useEffect(() => {
    const fetchTokens = async () => {
      const response = await fetch("/api/check_auth", {
        credentials: "include"
      })

      const json = await response.json()

      if(!response.ok){
        dispatch({type: "LOGOUT"})
        setError(json?.error)
      }
      if(response.ok){
        console.log("look: ", response)
        localStorage.setItem("refresh_token", response.refresh_token)
        dispatch({type: "LOGIN", payload:json})
      }
    }

    if(user){
      fetchTokens()
    }
  },[])
  return (
    

    <div>
      <AuthTests/>
      {user && <CalendarApiTest/>}
      {user && <EventApiTest/>}
      {user && <TaskApiTest/>}
    </div>
  )
}

export default App
