import React, { useEffect, useState } from 'react';

export default function AdminStatisticsPage() {
  const [books, setBooks] = useState([]);
  const [exchanges, setExchanges] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchData() {
      try {
        const booksRes = await fetch('http://127.0.0.1:5000/books');
        const booksData = await booksRes.json();
        if (!booksRes.ok) throw new Error('Ошибка загрузки книг');
        setBooks(booksData);

        const exRes = await fetch('http://127.0.0.1:5000/exchange');
        const exData = await exRes.json();
        if (!exRes.ok) throw new Error('Ошибка загрузки обменов');
        setExchanges(exData);
      } catch (err) {
        setError(err.message);
      }
    }

    fetchData();
  }, []);

  const accepted = exchanges.filter(e => e.status === 'accepted').length;
  const declined = exchanges.filter(e => e.status === 'declined').length;

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Статистика</h2>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}

      <ul>
        <li>Всего книг в системе: <strong>{books.length}</strong></li>
        <li>Всего обменов: <strong>{exchanges.length}</strong></li>
        <li>Завершённых (принятых): <strong>{accepted}</strong></li>
        <li>Отклонённых: <strong>{declined}</strong></li>
      </ul>
    </div>
  );
}
