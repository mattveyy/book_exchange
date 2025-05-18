import React, { useContext, useEffect, useState } from 'react';
import { UserContext } from '../context/UserContext';
import { getBooks, deleteBook } from '../api/books';
import './ProfilePage.css';

const ProfilePage = () => {
  const { user } = useContext(UserContext);
  const [myBooks, setMyBooks] = useState([]);
  const [error, setError] = useState('');
  const [editingBookId, setEditingBookId] = useState(null);
  const [editForm, setEditForm] = useState({});

  useEffect(() => {
    async function fetchMyBooks() {
      try {
        const allBooks = await getBooks();
        const filtered = allBooks.filter((book) => book.user_id === user.id);
        setMyBooks(filtered);
      } catch (err) {
        setError(err.message);
      }
    }
    fetchMyBooks();
  }, [user]);

  const handleDelete = async (bookId) => {
    if (!window.confirm('Удалить эту книгу?')) return;
    try {
      const res = await fetch(`http://127.0.0.1:5000/books/${bookId}`, {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json'
        }
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({ error: 'Ошибка удаления (не JSON)' }));
        throw new Error(data.error || 'Ошибка удаления');
      }

      setMyBooks((prev) => prev.filter((b) => b.id !== bookId));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEditChange = (e) => {
    setEditForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleEditSubmit = async (bookId) => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/books/${bookId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editForm),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Ошибка редактирования');

      setMyBooks((prev) =>
        prev.map((book) =>
          book.id === bookId ? { ...book, ...editForm } : book
        )
      );
      setEditingBookId(null);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="profile-container">
      <h2>Мои книги</h2>
      {error && <p className="form-error">{error}</p>}
      <div className="book-list">
        {myBooks.length === 0 ? (
          <p>У вас пока нет добавленных книг.</p>
        ) : (
          myBooks.map((book) => (
            <div className="book-card" key={book.id}>
              {editingBookId === book.id ? (
                <>
                  <input
                    name="title"
                    value={editForm.title || ''}
                    onChange={handleEditChange}
                    placeholder="Название"
                  />
                  <input
                    name="author"
                    value={editForm.author || ''}
                    onChange={handleEditChange}
                    placeholder="Автор"
                  />
                  <input
                    name="genre"
                    value={editForm.genre || ''}
                    onChange={handleEditChange}
                    placeholder="Жанр"
                  />
                  <input
                    name="location"
                    value={editForm.location || ''}
                    onChange={handleEditChange}
                    placeholder="Местоположение"
                  />
                  <textarea
                    name="description"
                    value={editForm.description || ''}
                    onChange={handleEditChange}
                    placeholder="Описание"
                  />
                  <div className="card-buttons">
                    <button className="delete" onClick={() => handleEditSubmit(book.id)}>Сохранить</button>
                    <button className="edit" onClick={() => setEditingBookId(null)}>Отмена</button>
                  </div>
                </>
              ) : (
                <>
                  <h3>{book.title}</h3>
                  <p><strong>Автор:</strong> {book.author}</p>
                  {book.genre && <p><strong>Жанр:</strong> {book.genre}</p>}
                  {book.location && <p><strong>Местоположение:</strong> {book.location}</p>}
                  {book.description && <p><strong>Описание:</strong> {book.description}</p>}
                  <p><strong>Статус:</strong> {book.status === 'available' ? 'Доступна' : 'Недоступна'}</p>
                  <div className="card-buttons">
                    <button className="delete" onClick={() => handleDelete(book.id)}>Удалить</button>
                    <button className="edit" onClick={() => {
                      setEditingBookId(book.id);
                      setEditForm({
                        title: book.title,
                        author: book.author,
                        genre: book.genre || '',
                        location: book.location || '',
                        description: book.description || '',
                      });
                    }}>Редактировать</button>
                  </div>
                </>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ProfilePage;
