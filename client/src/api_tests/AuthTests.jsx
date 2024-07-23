import React, { useState } from 'react'
import { useLogin } from '../hooks/useLogin'
import { useLogout } from '../hooks/useLogout'
import { useAuthContext } from '../hooks/useAuthContext'

const AuthTests = () => {

  const [isError, setIsError] = useState(null)
  const {login, error, isLoading} = useLogin()
  const { logout } = useLogout()
  const {user} = useAuthContext()

  const handleLogin = async (e) => {
  e.preventDefault()
  
    await login('user1@gmail.com', 'password123')
  }

  const handle_check_session = async () => {
    const response = await fetch('/api/check_session', {
      headers: {
        Authorization: `bearer ${user.token}`
      }
    })

    const json = await response.json()

    if(!response.ok || !json){
      setIsError(json?.error || 'error occurred')
      alert(error)

    }
    if(response.ok){
      console.log(json)
    }
  }

  return (
    <div>
        <button onClick={(e) => handleLogin(e)}>Log in</button>
        <button onClick={() => logout(user)}>Log out</button>
        <button onClick={() => handle_check_session()}>Check Session</button>
    </div>
  )
}

export default AuthTests