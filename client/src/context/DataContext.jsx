import { createContext, useReducer } from "react"

export const CalendarContext = createContext()
export const TaskContext = createContext()
export const EventContext = createContext()
// export const Sent_InviteContext = createContext()
// export const Received_InviteContext = createContext()
// export const Owned_CollaborationContext = createContext()
// export const Guest_CollaborationContext = createContext()

const createReducer = (entity) => (state, action) => {
    switch(action.type) {
        case `SET_${entity}`:
            return { 
                [entity.toLowerCase()]: action.payload 
            }
        case `CREATE_${entity}`:
            return {
                [entity.toLowerCase()]: [action.payload, ...state[entity.toLowerCase()]]
            }
        case `UPDATE_${entity}`:
            return {
                [entity.toLowerCase()]: state[entity.toLowerCase()].map((item) => {
                    return item.id === action.payload.id ? action.payload : item
                })
            }
        case `DELETE_${entity}`:
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

// const CalendarReducer = createReducer('CALENDARS')
// const TaskReducer = createReducer('TASKS')
// const EventReducer = createReducer('EVENTS')
// const OwnedCollaborationReducer = createReducer('OWNED_COLLABORATIONS')
// const GuestCollaborationReducer = createReducer('GUEST_COLLABORATIONS')



// export const CalendarContextProvider = createProvider(CalendarContext, CalendarReducer, { calendars: [] })
// export const TaskContextProvider = createProvider(TaskContext, TaskReducer, { tasks: [] })
// export const EventContextContextProvider = createProvider(EventContext, EventReducer, { events: [] })
// export const OwnedCollaborationContextProvider = createProvider(Owned_CollaborationContext, OwnedCollaborationReducer, { owned_collaborations: [] })
// export const GuestCollaborationContextProvider = createProvider(Guest_CollaborationContext, GuestCollaborationReducer, { guest_collaborations: [] })
