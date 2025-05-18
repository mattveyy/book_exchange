import React, { useEffect, useState, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import './ExchangePage.css';

const statusMap = {
  pending: 'В ожидании',
  accepted: 'Принята',
  declined: 'Отклонена',
};

const IncomingRequestsPage = () => {
  const { user } = useContext(UserContext);
  const [requests, setRequests] = useState([]);
  const [error, setError] = useState('');

  const fetchRequests = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/exchange/incoming?user_id=${user.id}`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Ошибка при получении');
      setRequests(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    if (user?.id) fetchRequests();
  }, [user]);

  const updateStatus = async (id, status) => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/exchange/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) throw new Error('Ошибка обновления');
      fetchRequests();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="exchange-container">
      <h2>Входящие заявки</h2>
      {error && <p className="form-error">{error}</p>}
      <ul className="exchange-list">
        {requests.length === 0 ? (
          <p>Нет входящих заявок</p>
        ) : (
          requests.map((r) => (
            <li key={r.id} className="exchange-item">
              <p><strong>Пользователь:</strong> {r.from_user}</p>
              <p><strong>Предлагает:</strong> {r.offered_book_title}</p>
              <p><strong>В обмен на:</strong> {r.requested_book_title}</p>
              <p><strong>Статус:</strong> {statusMap[r.status] || r.status}</p>
              {r.status === 'pending' && (
                <div className="action-buttons">
                  <button className="accept-btn" onClick={() => updateStatus(r.id, 'accepted')}>
                    Принять
                  </button>
                  <button className="decline-btn" onClick={() => updateStatus(r.id, 'declined')}>
                    Отклонить
                  </button>
                </div>
              )}
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default IncomingRequestsPage;
