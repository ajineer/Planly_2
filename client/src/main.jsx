import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { AuthContextProvider } from './context/AuthContext.jsx'
import { CalendarContextProvider, TaskContextProvider, EventContextProvider } from './context/CalendarEventTaskContext.jsx'
import { SentInviteContextProvider, ReceivedInviteContextProvider } from './context/InviteContext.jsx'
import { CollaborationContextProvider } from './context/CollaborationContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthContextProvider>
      <CalendarContextProvider>
        <TaskContextProvider>
          <EventContextProvider>
            <SentInviteContextProvider>
              <ReceivedInviteContextProvider>
                <CollaborationContextProvider>
                  <App />
                </CollaborationContextProvider>    
              </ReceivedInviteContextProvider>
            </SentInviteContextProvider>
          </EventContextProvider>
        </TaskContextProvider>
      </CalendarContextProvider>
    </AuthContextProvider>
  </React.StrictMode>
)
