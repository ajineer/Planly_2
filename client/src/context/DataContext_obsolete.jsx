// import { createContext, useReducer } from "react";

// export const CalendarContext = createContext()
// export const EventContext = createContext()
// export const TaskContext = createContext()
// export const OwnedCollaborationContext = createContext()
// export const GuestCollaborationContext = createContext()
// export const SentInviteContext = createContext()
// export const ReceivedInviteContext = createContext()

// export const CalendarReducer = (state, action) => {
//     switch (action.type) {
//         case 'SET_CALENDARS':
//             return {
//                 calendars: action.payload
//             }
//         case 'CREATE_CALENDAR':
//             return {
//                 calendars: [action.payload, ...state.calendars]
//             }
//         case 'UPDATE_CALENDAR':
//             return {
//                 calendars: state.calendars.map(c => {
//                     return c.id === action.payload.id ? action.payload : c
//                 })
//             }

//         case 'DELETE_CALENDAR':
//             return {
//                 calendars: state.calendars.filter((c) => c.id !== action.payload.id)
//             }
//     }
// }

// export const EventReducer = (state, action) => {
//     switch(action.type){

//         case 'SET_EVENTS':
//             return {
//                 events: action.payload
//             }
//         case 'CREATE_EVENT':
//             return {
//                 events: [action.payload, ...state.events]
//             }
//         case 'UPDATE_EVENT':
//             return {
//                 events: state.events.map((e) => e.id === action.payload.id ? action.payload : e)
//             }
//         case 'DELETE_EVENT':
//             return {
//                 events: state.events.filter((e) => e.id !== action.payload.id)
//             }
//     }
// }

// export const TaskReducer = (state, action) => {
//     switch(action.type){

//         case 'SET_TASKS':
//             return {
//                 tasks: action.payload
//             }
//         case 'CREATE_TASK':
//             return {
//                 tasks: [action.payload, ...state.tasks]
//             }
//         case 'UPDATE_TASK':
//             return {
//                 tasks: state.tasks.map((t) => t.id === action.payload.id ? action.payload : t)
//             }
//         case 'DELETE_TASK':
//             return {
//                 tasks: state.tasks.filter((t) => t.id !== action.payload.id)
//             }
//     }
// }

// export const SentInviteReducer = (state, action) => {
//     switch(action.type){
//         case 'SET_INVITES':
//             return {
//                 sent_invites: action.payload
//             }
//         case 'CREATE_INVITES':
//             return {
//                 sent_invites: [action.payload, ...state.sent_invites]
//             }
//         case 'DELETE_INVITE':
//             return {
//                 sent_invites: state.sent_invites.filter((i) => i.id !== action.payload.id)
//             }
//     }
// }
// export const ReceivedInviteReducer = (state, action) => {
//     switch(action.type){
//         case 'SET_INVITES':
//             return {
//                 received_invites: action.payload
//             }
//         case 'UPDATE_INVITE':
//             return {
//                 received_invites: received_invites.filter((i) => i.id === action.payload.id ? action.payload : i)
//             }
//         case 'DELETE_INVITE':
//             return {
//                 received_invites: state.received_invites.filter((i) => i.id !== action.payload.id)
//             }
//     }
// }

// export const OwnedCollaborationReducer = (state, action) => {
//     switch(action.type){
//         case 'SET_COLLABORATIONS':
//             return {
//                 owned_collaborations: action.payload
//             }
//         case 'UPDATE_COLLABORATION':
//             return {
//                 owned_collaborations: state.owned_collaborations.map((c) => c.id === action.payload.id ? action.payload : c)
//             }
//         case 'DELETE_COLLABORATION':
//             return { 
//                 owned_collaborations: state.owned_collaborations.filter((c) => c.id !== action.payload.id)
//             }
//     }
// }

// export const GuestCollaborationReducer = (state, action) => {
//     switch(action.type){
//         case 'SET_COLLABORATIONS':
//             return {
//                 guest_collaborations: action.payload
//             }
//         case 'DELETE_COLLABORATION':
//             return { 
//                 guest_collaborations: state.guest_collaborations.filter((c) => c.id !== action.payload.id)
//         }
//     }
// }

// export const CalendarContextProvider = ({ children }) => {
//     const [state, dispatch] = useReducer(CalendarReducer , {
//         calendars: []
//     })
//     return (
//         <CalendarContext.Provider value={{...state, dispatch}}>
//             { children }
//         </CalendarContext.Provider>
//     )
// }
// export const EventContextProvider = ({ children }) => {
//     const [state, dispatch] = useReducer(EventReducer , {
//         events: []
//     })
//     return (
//         <EventContext.Provider value={{...state, dispatch}}>
//             { children }
//         </EventContext.Provider>
//     )
// }
// export const TaskContextProvider = ({ children }) => {
//     const [state, dispatch] = useReducer(TaskReducer , {
//         tasks: []
//     })
//     return (
//         <TaskContext.Provider value={{...state, dispatch}}>
//             { children }
//         </TaskContext.Provider>
//     )
// }

// export const SentInviteContextProvider = ({ children }) => {
//     const [state, dispatch] = useReducer( SentInviteReducer, {
//         sent_invites:[]
//     })
//     return (
//         <SentInviteContextProvider.Provider value ={{...state, dispatch}}>
//             { children }
//         </SentInviteContextProvider.Provider>
//     )
// }
// export const ReceivedInviteContextProvider = ({ children }) => {
//     const [state, dispatch] = useReducer( ReceivedInviteReducer, {
//         received_invites:[]
//     })
//     return (
//         <ReceivedInviteContextProvider.Provider value ={{...state, dispatch}}>
//             { children }
//         </ReceivedInviteContextProvider.Provider>
//     )
// }
// export const GuestCollaborationContextProvider = ({ children }) => {
//     const [state, dispatch] = useReducer( GuestCollaborationReducer, {
//         guest_collaborations:[]
//     })
//     return (
//         <GuestCollaborationContextProvider.Provider value ={{...state, dispatch}}>
//             { children }
//         </GuestCollaborationContextProvider.Provider>
//     )
// }
// export const OwnedCollaborationContextProvider = ({ children }) => {
//     const [state, dispatch] = useReducer( OwnedCollaborationReducer, {
//         owned_collaborations:[]
//     })
//     return (
//         <OwnedCollaborationContextProvider.Provider value ={{...state, dispatch}}>
//             { children }
//         </OwnedCollaborationContextProvider.Provider>
//     )
// }