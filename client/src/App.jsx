import AuthTests from './api_tests/AuthTests'
import GetCalendars from './api_tests/GetCalendars'
import TaskApiTest from './api_tests/TaskApiTest'
import './App.css'

function App() {

  
  return (
    
    <div>
      <AuthTests/>
      <GetCalendars/>
      <TaskApiTest/>
    </div>
  )
}

export default App
