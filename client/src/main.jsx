import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { AuthContextProvider } from './context/AuthContext.jsx'
import { CalendarContextProvider, TaskContextProvider } from './context/DataContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthContextProvider>
      <CalendarContextProvider>
        <TaskContextProvider>
          {/* <EventContextContextProvider> */}
            {/* <SentInviteContextProvider> */}
              {/* <ReceivedInviteContextProvider> */}
                {/* <OwnedCollaborationContextProvider> */}
                    {/* <GuestCollaborationContextProvider> */}
        <App />
                    {/* </GuestCollaborationContextProvider> */}
                {/* </OwnedCollaborationContextProvider> */}
              {/* </ReceivedInviteContextProvider> */}
            {/* </SentInviteContextProvider> */}
          {/* </EventContextContextProvider> */}
        </TaskContextProvider>
      </CalendarContextProvider>
    </AuthContextProvider>
  </React.StrictMode>,
)
