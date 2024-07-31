import AuthTests from './api_tests/AuthTests'
import CalendarApiTest from './api_tests/CalendarApiTest'
import EventApiTest from './api_tests/EventApiTest'
import TaskApiTest from './api_tests/TaskApiTest'
import './App.css'

function App() {

  
  return (
    
    <div>
      <AuthTests/>
      <CalendarApiTest/>
      <EventApiTest/>
      <TaskApiTest/>
    </div>
  )
}

export default App
