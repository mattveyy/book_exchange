import React, { useEffect, useState, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import './ExchangePage.css';

const statusMap = {
  pending: 'В ожидании',
  accepted: 'Принята',
  declined: 'Отклонена',
};

const OutgoingRequestsPage = () => {
  const { user } = useContext(UserContext);
  const [requests, setRequests] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!user?.id) return;

    async function fetchRequests() {
      try {
        const res = await fetch(`http://127.0.0.1:5000/exchange/outgoing?user_id=${user.id}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Ошибка загрузки заявок');
        setRequests(data);
      } catch (err) {
        setError(err.message);
      }
    }

    fetchRequests();
  }, [user]);

  return (
    <div className="exchange-container">
      <h2>Отправленные заявки</h2>
      {error && <p className="form-error">{error}</p>}
      {requests.length === 0 ? (
        <p>Вы не отправляли заявки</p>
      ) : (
        <ul className="exchange-list">
          {requests.map((req) => (
            <li key={req.id} className="exchange-item">
              <div><strong>Вы предлагаете:</strong> {req.offered_book_title}</div>
              <div><strong>В обмен на:</strong> {req.requested_book_title}</div>
              <div><strong>Владелец книги:</strong> {req.to_user}</div>
              <div><strong>Статус:</strong> {statusMap[req.status] || req.status}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default OutgoingRequestsPage;
