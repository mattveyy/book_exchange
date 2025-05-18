import React, { useContext } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';
import "./Navbar.css";

export default function Navbar() {
  const { user, logoutUser } = useContext(UserContext);
  const location = useLocation();
  const navigate = useNavigate();

  if (location.pathname === '/admin') return null;

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/" className="navbar-logo">📚 <strong>BookExchange</strong></Link>
        {user && <Link to="/profile">Профиль</Link>}
        <Link to="/books">Книги</Link>

        {user && user.role !== 'admin' && (
          <>
            <Link to="/add-book">Добавить книгу</Link>
            <Link to="/exchange/incoming">Входящие заявки</Link>
            <Link to="/exchange/outgoing">Мои заявки</Link>
          </>
        )}

        {user?.role === 'admin' && (
          <Link to="/admin">Статистика</Link>
        )}
      </div>
      <div className="navbar-right">
        {!user ? (
          <>
            <Link to="/login">Вход</Link>
            <Link to="/register">Регистрация</Link>
          </>
        ) : (
          <>
            <span className="navbar-user">Привет, {user.username}</span>
            <button
              className="navbar-btn"
              onClick={() => {
                logoutUser();
                navigate('/');
              }}
            >Выйти</button>
          </>
        )}
      </div>
    </nav>
  );
}
