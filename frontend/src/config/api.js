import axios from 'axios'


const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor untuk menambahkan token ke header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor untuk menangani response
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Jika mendapat error 401, clear localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
      
      // Redirect ke login page
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default api 
