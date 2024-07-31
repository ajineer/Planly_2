import React, { useState } from 'react'
import { useLogin } from '../hooks/useLogin'
import { useLogout } from '../hooks/useLogout'

const AuthTests = () => {

  const {login, error, isLoading} = useLogin()
  const { logout } = useLogout()

  const handleLogin = async (e) => {
  e.preventDefault()
  
    await login('user1@gmail.com', 'password123')
  }

  return (
    <div>
        <button onClick={(e) => handleLogin(e)}>Log in</button>
        {error && <h3>{error}</h3>}
        <button onClick={() => logout()}>Log out</button>
    </div>
  )
}

export default AuthTests