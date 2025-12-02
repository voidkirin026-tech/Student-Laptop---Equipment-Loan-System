import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    // CSRF token handling if needed
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 unauthorized - redirect to login
    if (error.response?.status === 401) {
      // Clear auth context and redirect
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication endpoints
export const authService = {
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  
  register: (email, password, full_name, student_id, phone) =>
    api.post('/auth/register', {
      email,
      password,
      full_name,
      student_id,
      phone,
    }),
  
  logout: () =>
    api.post('/auth/logout'),
  
  getCurrentUser: () =>
    api.get('/auth/current-user'),
};

// Equipment endpoints
export const equipmentService = {
  getAll: () =>
    api.get('/equipment'),
  
  getById: (id) =>
    api.get(`/equipment/${id}`),
  
  create: (data) =>
    api.post('/equipment', data),
  
  update: (id, data) =>
    api.put(`/equipment/${id}`, data),
  
  delete: (id) =>
    api.delete(`/equipment/${id}`),
  
  getAvailable: () =>
    api.get('/equipment/available'),
};

// Student endpoints
export const studentService = {
  getAll: () =>
    api.get('/students'),
  
  getById: (id) =>
    api.get(`/students/${id}`),
  
  create: (data) =>
    api.post('/students', data),
  
  update: (id, data) =>
    api.put(`/students/${id}`, data),
  
  delete: (id) =>
    api.delete(`/students/${id}`),
  
  getProfile: () =>
    api.get('/students/profile'),
};

// Loan endpoints
export const loanService = {
  getAll: () =>
    api.get('/loans'),
  
  getById: (id) =>
    api.get(`/loans/${id}`),
  
  create: (data) =>
    api.post('/loans', data),
  
  update: (id, data) =>
    api.put(`/loans/${id}`, data),
  
  checkout: (data) =>
    api.post('/loans/checkout', data),
  
  returnItem: (loan_id, data) =>
    api.post(`/loans/${loan_id}/return`, data),
  
  renew: (id) =>
    api.post(`/loans/${id}/renew`),
  
  getOverdue: () =>
    api.get('/loans/overdue'),
};

// Reservation endpoints
export const reservationService = {
  getAll: () =>
    api.get('/reservations'),
  
  getById: (id) =>
    api.get(`/reservations/${id}`),
  
  create: (data) =>
    api.post('/reservations', data),
  
  cancel: (id) =>
    api.delete(`/reservations/${id}`),
  
  getByEquipment: (equipment_id) =>
    api.get(`/reservations/equipment/${equipment_id}`),
  
  getByStudent: (student_id) =>
    api.get(`/reservations/student/${student_id}`),
};

// Damage log endpoints
export const damageService = {
  getAll: () =>
    api.get('/damage-logs'),
  
  getById: (id) =>
    api.get(`/damage-logs/${id}`),
  
  create: (data) =>
    api.post('/damage-logs', data),
  
  getByLoan: (loan_id) =>
    api.get(`/damage-logs/loan/${loan_id}`),
  
  getByStudent: (student_id) =>
    api.get(`/damage-logs/student/${student_id}`),
};

// Report endpoints
export const reportService = {
  getEquipmentStatus: () =>
    api.get('/reports/equipment-status'),
  
  getLoanActivity: () =>
    api.get('/reports/loan-activity'),
  
  getOverdueAnalysis: () =>
    api.get('/reports/overdue-analysis'),
  
  getDamageAnalysis: () =>
    api.get('/reports/damage-analysis'),
  
  getStudentActivity: () =>
    api.get('/reports/student-activity'),
};

export default api;
