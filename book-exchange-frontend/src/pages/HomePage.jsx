import React, { useContext } from 'react';
import { UserContext } from '../context/UserContext';
import './HomePage.css';

const HomePage = () => {
  const { user } = useContext(UserContext);

  return (
    <div className="home-container">
      <h1>Добро пожаловать в BookExchange!</h1>
      {user ? (
        <p>Рады видеть тебя снова, {user.username}</p>
      ) : (
        <p>Чтобы начать обмен книгами — войдите или зарегистрируйтесь.</p>
      )}
      <img
        src="/images/exchange_illustration.png"
        alt="Обмен книгами"
        style={{ maxWidth: '700px', width: '100%', margin: '2rem auto 0', display: 'block', borderRadius: '16px', boxShadow: '0 2px 8px rgba(62,47,28,0.08)' }}
      />
    </div>
  );
};

export default HomePage;
