import { createContext, useReducer } from "react"

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

const CalendarReducer = createReducer('CALENDARS')
const EventReducer = createReducer('EVENTS')
const TaskReducer = createReducer('TASKS')

export const CalendarContext = createContext()
export const EventContext = createContext()
export const TaskContext = createContext()
export const CalendarContextProvider = createProvider(CalendarContext, CalendarReducer, { calendars: [] })
export const TaskContextProvider = createProvider(TaskContext, TaskReducer, { tasks: [] })
export const EventContextContextProvider = createProvider(EventContext, EventReducer, { events: [] })