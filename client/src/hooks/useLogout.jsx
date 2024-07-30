import { useState } from "react";
import { useAuthContext } from "./useAuthContext";

export const useLogout = () => {

    const { dispatch } = useAuthContext()

    const logout = () => {
        localStorage.removeItem('user_token')
        dispatch({type: 'LOGOUT'})
    }

    return { logout }
}