import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Emergency from './pages/Emergency'
import Contacts from './pages/Contacts'
import BodyMap from './pages/BodyMap'
import FirstAidKit from './pages/FirstAidKit'
import Quiz from './pages/Quiz'
import AIAssistant from './pages/AIAssistant'
import Preparedness from './pages/Preparedness'
import EmergencyWorkflow from './pages/EmergencyWorkflow'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/emergency" element={<Emergency />} />
          <Route path="/emergency/:type" element={<EmergencyWorkflow />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/body-map" element={<BodyMap />} />
          <Route path="/first-aid-kit" element={<FirstAidKit />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/ai-assistant" element={<AIAssistant />} />
          <Route path="/preparedness" element={<Preparedness />} />
          <Route path="/preparedness/:topic" element={<Preparedness />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
