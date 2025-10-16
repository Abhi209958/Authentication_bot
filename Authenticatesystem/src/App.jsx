import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './components/Login'
import Register from './components/Register'
import Chat from './components/Chat'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setIsAuthenticated(true)
    }
    setLoading(false)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route 
            path="/login" 
            element={
              !isAuthenticated ? 
              <Login setIsAuthenticated={setIsAuthenticated} /> : 
              <Navigate to="/chat" />
            } 
          />
          <Route 
            path="/register" 
            element={
              !isAuthenticated ? 
              <Register setIsAuthenticated={setIsAuthenticated} /> : 
              <Navigate to="/chat" />
            } 
          />
          <Route 
            path="/chat" 
            element={
              isAuthenticated ? 
              <Chat setIsAuthenticated={setIsAuthenticated} /> : 
              <Navigate to="/login" />
            } 
          />
          <Route 
            path="/" 
            element={
              isAuthenticated ? 
              <Navigate to="/chat" /> : 
              <Navigate to="/login" />
            } 
          />
        </Routes>
      </div>
    </Router>
  )
}

export default App
