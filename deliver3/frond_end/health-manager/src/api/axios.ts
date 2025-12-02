import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  withCredentials: true, // Important for session cookies
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
