// Use relative path for same-origin requests
const API_BASE_URL = '/api';

// Generic fetch wrapper
async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}

// Contacts API
export const contactsApi = {
  getAll: () => apiFetch('/contacts'),
  add: (contact: { name: string; phone: string; relationship: string }) =>
    apiFetch('/contacts', { method: 'POST', body: JSON.stringify(contact) }),
  update: (id: number, contact: Partial<{ name: string; phone: string; relationship: string }>) =>
    apiFetch(`/contacts/${id}`, { method: 'PUT', body: JSON.stringify(contact) }),
  delete: (id: number) => apiFetch(`/contacts/${id}`, { method: 'DELETE' }),
};

// First Aid Items API
export const firstAidApi = {
  getAll: () => apiFetch('/first-aid-items'),
  add: (item: { name: string; quantity: number; notes?: string }) =>
    apiFetch('/first-aid-items', { method: 'POST', body: JSON.stringify(item) }),
  update: (id: number, item: Partial<{ name: string; quantity: number; in_stock: boolean; notes: string }>) =>
    apiFetch(`/first-aid-items/${id}`, { method: 'PUT', body: JSON.stringify(item) }),
  delete: (id: number) => apiFetch(`/first-aid-items/${id}`, { method: 'DELETE' }),
};

// Quiz API
export const quizApi = {
  getQuestions: (category?: string) =>
    apiFetch(category ? `/quiz/questions?category=${category}` : '/quiz/questions'),
  submitResult: (result: { category: string; score: number; total: number; answers: number[] }) =>
    apiFetch('/quiz/submit', { method: 'POST', body: JSON.stringify(result) }),
  getResults: () => apiFetch('/quiz/results'),
};

// Body Parts API
export const bodyPartsApi = {
  getAll: () => apiFetch('/body-parts'),
  getOne: (partId: string) => apiFetch(`/body-parts/${partId}`),
};

// Emergencies API
export const emergenciesApi = {
  getAll: () => apiFetch('/emergencies'),
  getOne: (type: string) => apiFetch(`/emergencies/${type}`),
};

// Preparedness API
export const preparednessApi = {
  getAll: () => apiFetch('/preparedness'),
  getOne: (guideId: string) => apiFetch(`/preparedness/${guideId}`),
};

// Health check
export const healthCheck = () => apiFetch('/health');
