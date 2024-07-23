import { useState } from "react";
import { useAuthContext } from "./useAuthContext";

export const useLogout = () => {

    const [error, setError] = useState(null)
    const [isLoading, setIsLoading] = useState(null)
    const { dispatch } = useAuthContext()

    const logout = async (user) => {

        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                Authorization: `bearer ${user.token}`
            }
        })


        const json = await response.json()
        if(!response.ok || !json){
            setIsLoading(false)
            setError(json?.error || 'error occurred')
        }

        if(response.ok){
            localStorage.setItem('user_token', JSON.stringify(json))
            dispatch({type: 'LOGOUT'})
            setIsLoading(false)
        }
    }

    return { logout, isLoading, error }
}