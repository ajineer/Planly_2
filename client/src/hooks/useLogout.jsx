import { useState } from "react";
import { useAuthContext } from "./useAuthContext";

export const useLogout = () => {

    const { dispatch } = useAuthContext()

    const logout = () => {
        localStorage.removeItem('refresh_token')
        dispatch({type: 'LOGOUT'})
    }

    return { logout }
}