import React, { useEffect, useState, useContext } from 'react';
import { getBooks } from '../api/books';
import { UserContext } from '../context/UserContext';
import './BooksPage.css';

const BooksPage = () => {
  const [books, setBooks] = useState([]);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({ author: '', genre: '', title: '' });
  const [sortAsc, setSortAsc] = useState(true);
  const [requestedIds, setRequestedIds] = useState([]);
  const { user } = useContext(UserContext);

  useEffect(() => {
    async function fetchBooks() {
      try {
        const data = await getBooks();
        setBooks(data);
      } catch (err) {
        setError(err.message);
      }
    }
    fetchBooks();
  }, []);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleResetFilters = () => {
    setFilters({ author: '', genre: '', title: '' });
  };

  const handleToggleSort = () => {
    setSortAsc((prev) => !prev);
  };

  const handleExchangeRequest = async (requestedBookId, receiverId, offeredBookId) => {
    try {
      const res = await fetch('http://127.0.0.1:5000/exchange/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          requested_book_id: requestedBookId,
          offered_book_id: offeredBookId,
          sender_id: user.id,
          receiver_id: receiverId,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Ошибка обмена');

      alert('Заявка отправлена');
      setRequestedIds((prev) => [...prev, requestedBookId]);
    } catch (err) {
      alert(err.message);
    }
  };

  const filteredBooks = books
    .filter((book) =>
      book.title.toLowerCase().includes(filters.title.toLowerCase()) &&
      book.author.toLowerCase().includes(filters.author.toLowerCase()) &&
      book.genre?.toLowerCase().includes(filters.genre.toLowerCase())
    )
    .sort((a, b) =>
      sortAsc
        ? a.title.localeCompare(b.title)
        : b.title.localeCompare(a.title)
    );

  const myAvailableBooks = books.filter(
    (b) => b.user_id === user?.id && b.status === 'available'
  );

  return (
    <div className="books-container">
      <h2>Доступные книги для обмена</h2>

      <div className="filter-bar">
        <input
          type="text"
          name="title"
          placeholder="Фильтр по названию"
          value={filters.title}
          onChange={handleFilterChange}
        />
        <input
          type="text"
          name="author"
          placeholder="Фильтр по автору"
          value={filters.author}
          onChange={handleFilterChange}
        />
        <input
          type="text"
          name="genre"
          placeholder="Фильтр по жанру"
          value={filters.genre}
          onChange={handleFilterChange}
        />
        <button className="filter-btn" onClick={handleResetFilters}>Сбросить</button>
        <button className="filter-btn" onClick={handleToggleSort}>
          Сортировать {sortAsc ? '↓' : '↑'}
        </button>
      </div>

      {error && <p className="form-error">{error}</p>}

      <div className="book-list">
        {filteredBooks.map((book) => (
          <div className="book-card" key={book.id}>
            <h3>{book.title}</h3>
            <p><strong>Автор:</strong> {book.author}</p>
            {book.genre && <p><strong>Жанр:</strong> {book.genre}</p>}
            {book.location && <p><strong>Местоположение:</strong> {book.location}</p>}
            {book.description && <p><strong>Описание:</strong> {book.description}</p>}
            <p><strong>Статус:</strong> {book.status === 'available' ? 'Доступна' : 'Недоступна'}</p>

            {user && book.user_id !== user.id && (
              <div className="exchange-action">
                <select
                  onChange={(e) => {
                    const offeredId = e.target.value;
                    if (offeredId) {
                      handleExchangeRequest(book.id, book.user_id, offeredId);
                    }
                  }}
                  disabled={requestedIds.includes(book.id)}
                >
                  <option value="">Выбери свою книгу</option>
                  {myAvailableBooks.map((own) => (
                    <option key={own.id} value={own.id}>
                      {own.title}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BooksPage;
