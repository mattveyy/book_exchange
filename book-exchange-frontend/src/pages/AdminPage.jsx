import React, { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import './AdminPage.css';

export default function AdminPage() {
  const { user } = useContext(UserContext);
  const navigate = useNavigate();

  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  useEffect(() => {
    if (user?.role === 'admin') {
      navigate('/admin/statistics');
    }
  }, [user, navigate]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        throw new Error('Неверный логин или пароль');
      }

      const data = await res.json();
      if (data.user.role !== 'admin') {
        throw new Error('Недостаточно прав');
      }

      localStorage.setItem('user', JSON.stringify(data.user));
      window.location.href = '/admin/statistics';
    } catch (err) {
      setError(err.message);
    }
  };

  if (user && user.role !== 'admin') {
    return (
      <div className="admin-container">
        <p className="admin-error">Доступ запрещён</p>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <form onSubmit={handleSubmit} className="admin-form">
        <h2>Вход в админку</h2>
        <input
          type="text"
          name="username"
          placeholder="Логин"
          value={form.username}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Пароль"
          value={form.password}
          onChange={handleChange}
          required
        />
        {error && <p className="admin-error">{error}</p>}
        <button type="submit">Войти</button>
      </form>
    </div>
  );
}
