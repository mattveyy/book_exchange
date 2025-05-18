import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import './AddBookPage.css';

const AddBookPage = () => {
  const { user } = useContext(UserContext);
  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: '',
    author: '',
    genre: '',
    description: '',
    location: '',
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.title.trim() || !form.author.trim()) {
      setError('Поля "Название" и "Автор" обязательны');
      return;
    }

    try {
      const res = await fetch('http://127.0.0.1:5000/books/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...form,
          user_id: user?.id,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Ошибка добавления книги');

      navigate('/books');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="addbook-container">
      <form className="addbook-form" onSubmit={handleSubmit}>
        <h2>Предложить книгу для обмена</h2>

        <input
          type="text"
          name="title"
          placeholder="Название книги"
          value={form.title}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="author"
          placeholder="Автор"
          value={form.author}
          onChange={handleChange}
          required
        />

        <select
          name="genre"
          value={form.genre}
          onChange={handleChange}
        >
          <option value="">Выберите жанр</option>
          <option value="Роман">Роман</option>
          <option value="Фантастика">Фантастика</option>
          <option value="Детектив">Детектив</option>
          <option value="Фэнтези">Фэнтези</option>
          <option value="Приключения">Приключения</option>
          <option value="Научная литература">Научная литература</option>
          <option value="Биография">Биография</option>
          <option value="История">История</option>
          <option value="Поэзия">Поэзия</option>
          <option value="Драма">Драма</option>
          <option value="Другое">Другое</option>
        </select>

        <select
          name="location"
          value={form.location}
          onChange={handleChange}
        >
          <option value="">Выберите местоположение</option>
          <option value="Библиотека">Библиотека</option>
          <option value="Коворкинг ВК">Коворкинг ВК</option>
          <option value="4 этаж">4 этаж</option>
        </select>

        <textarea
          name="description"
          placeholder="Описание"
          rows="4"
          value={form.description}
          onChange={handleChange}
        />

        {error && <p className="form-error">{error}</p>}

        <button type="submit">Добавить книгу</button>
      </form>
    </div>
  );
};

export default AddBookPage;
