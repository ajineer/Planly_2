import { createContext, useReducer } from "react"


const createInviteReducer = (entity) => (state, action) => {
    switch(action.type) {
        case "SET_INVITES":
            return {
                [entity.toLowerCase()]: action.payload
            }
        case "CREATE_INVITES":
            return {
                [entity.toLowerCase()]: [action.payload, ...state[entity.toLowerCase()]]
            }
        case "UPDATE_INVITES":
            return {
                [entity.toLowerCase]: state[entity.toLowerCase()].map((item) => {
                    return item.id === action.payload.id ? action.payload : item
                })
            }
        case "DELETE_INVITES":
            return {
                [entity.toLowerCase()]: state[entity.toLowerCase()].filter((item) => item.id !== action.payload.id)
            }
        }
    }
                
    const createProvider = (Context, reducer, intialState) => ({ children }) => {
        const [state, dispatch] = useReducer(reducer, intialState)
        return (
            <Context.Provider value={{ ...state, dispatch}}>
                {children}
            </Context.Provider>
        )
    }
const Sent_InviteReducer = createInviteReducer('SENT_INVITES')
const Received_InviteReducer = createInviteReducer('RECEIVED_INVITES')
                
export const Sent_InviteContext = createContext()
export const Received_InviteContext = createContext()
export const SentInviteContextProvider = createProvider(Sent_InviteContext, Sent_InviteReducer, { sent_invites: [] })
export const ReceivedInviteContextProvider = createProvider(Received_InviteContext, Received_InviteReducer, { received_invites: [] })