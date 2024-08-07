import { useState } from "react";

export const useLogin = () => {
    const [error, setError] = useState(null)
    const [isLoading, setIsLoading] = useState(null)

    const login = async (email, password) => {

        setIsLoading(true)
        setError(null)

        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password})
        })

        const json = await response.json()
        if(!response.ok || !json){
            setIsLoading(false)
            setError(json?.error || 'error occurred')
        }

        if(response.ok){
            setIsLoading(false)
        }
    }

    return { login, isLoading, error }
}

