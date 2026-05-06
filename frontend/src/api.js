const API_URL = 'http://localhost:8000'

function getAuthHeaders() {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function login(username, password) {
  const formData = new URLSearchParams()
  formData.append('username', username)
  formData.append('password', password)

  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Login failed')
  }
  
  return response.json()
}

export async function register(email, password) {
  const response = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Registration failed')
  }
  
  return response.json()
}

export async function getProjects() {
  const response = await fetch(`${API_URL}/projects`, {
    headers: getAuthHeaders()
  })
  
  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    throw new Error('Failed to fetch projects')
  }
  
  return response.json()
}

export async function getProject(projectId) {
  const response = await fetch(`${API_URL}/projects/${projectId}`, {
    headers: getAuthHeaders()
  })
  
  if (!response.ok) {
    throw new Error('Failed to fetch project details')
  }
  
  return response.json()
}

export async function uploadProject(title, file) {
  const formData = new FormData()
  formData.append('title', title)
  formData.append('file', file)

  const response = await fetch(`${API_URL}/upload_gdd`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: formData
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Upload failed')
  }
  
  return response.json()
}

export async function analyzeProject(projectId) {
  const response = await fetch(`${API_URL}/projects/${projectId}/analyze`, {
    method: 'POST',
    headers: getAuthHeaders()
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to start analysis')
  }
  
  return response.json()
}

export async function deleteProject(projectId) {
  const response = await fetch(`${API_URL}/projects/${projectId}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to delete project')
  }
  
  return true
}
