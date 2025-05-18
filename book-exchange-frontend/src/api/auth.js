const BASE_URL = 'http://127.0.0.1:5000';

export async function login(username, password) {
  const res = await fetch(`${BASE_URL}/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || error.message || 'Ошибка входа');
  }

  return res.json();
}

export async function register(username, email, password) {
  const res = await fetch(`${BASE_URL}/users/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || 'Ошибка регистрации');
  }

  return res.json();
}


