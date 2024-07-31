import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { CalendarContextProvider, TaskContextProvider, EventContextProvider } from './context/CalendarEventTaskContext.jsx'
import { SentInviteContextProvider, ReceivedInviteContextProvider } from './context/InviteContext.jsx'
import { CollaborationContextProvider } from './context/CollaborationContext.jsx'
import { BrowserRouter as Router } from 'react-router-dom'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
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
    </Router>
  </React.StrictMode>
)
