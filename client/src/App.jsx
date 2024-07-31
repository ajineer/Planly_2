import React, { useEffect, useState } from 'react'
import AuthTests from './api_tests/AuthTests'
// import CalendarApiTest from './api_tests/CalendarApiTest'
// import EventApiTest from './api_tests/EventApiTest'
// import TaskApiTest from './api_tests/TaskApiTest'
import './App.css'

function App() {

  const [authorized, setAuthorized] = useState(false)
  const {error, setError} = useState()

  useEffect(() => {
    const fetchToken = async () => {
      const response = await fetch("/api/check_auth", {
        credentials: "include"
      })

      const json = await response.json()

      if(!response.ok){
        console.log("user not logged in")
        setAuthorized(false)
        setError(json?.error)
      }
      if(response.ok){
        console.log("user logged in")
        setAuthorized(true)
      }
    }
    if(!authorized){
      fetchToken()
    }
  },[])
  return (
    

    <div>
      <AuthTests/>
      {/* <CalendarApiTest/>
      <EventApiTest/>
      <TaskApiTest/> */}
    </div>
  )
}

export default App
