import { useState } from "react"

export const useLogout = () => {

    const [error, setError] = useState(null)
    const logout = async () => {
        // document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
        const response = await fetch("/api/logout", {
            method: "POST",
            credentials:"include"
        })
        const json = await response.json()
        if(!response.ok){
            setError(json?.error)
        }
        if(response.ok){
            console.log("logout worked")
        }

    }

    return { logout, error }
}