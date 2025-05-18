import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';
import { UserContext } from '../context/UserContext';
import './LoginPage.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const { loginUser } = useContext(UserContext);

  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.username || !formData.password) {
      setError('Все поля обязательны');
      return;
    }

    try {
      const data = await login(formData.username, formData.password);
      loginUser({
        id: data.user_id,
        role: data.role,
        username: formData.username,
      });
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Вход в систему</h2>

        <input
          type="text"
          name="username"
          placeholder="Имя пользователя"
          value={formData.username}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Пароль"
          value={formData.password}
          onChange={handleChange}
          required
        />

        {error && <p className="form-error">{error}</p>}

        <button type="submit">Войти</button>

        <p className="switch-link">
          Нет аккаунта? <a href="/register">Зарегистрируйтесь</a>
        </p>
      </form>
    </div>
  );
};

export default LoginPage;
