import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import BooksPage from '../pages/BooksPage';
import AddBookPage from '../pages/AddBookPage';
import ProfilePage from '../pages/ProfilePage';
import IncomingRequestsPage from '../pages/IncomingRequestsPage';
import OutgoingRequestsPage from '../pages/OutgoingRequestsPage';
import AdminPage from '../pages/AdminPage';
import AdminStatisticsPage from '../pages/AdminStatisticsPage';
import Navbar from '../components/Navbar';

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <>
        <Navbar />
        <HomePage />
      </>
    ),
  },
  {
    path: '/login',
    element: (
      <>
        <Navbar />
        <LoginPage />
      </>
    ),
  },
  {
    path: '/register',
    element: (
      <>
        <Navbar />
        <RegisterPage />
      </>
    ),
  },
  {
    path: '/books',
    element: (
      <>
        <Navbar />
        <BooksPage />
      </>
    ),
  },
  {
    path: '/add-book',
    element: (
      <>
        <Navbar />
        <AddBookPage />
      </>
    ),
  },
  {
    path: '/profile',
    element: (
      <>
        <Navbar />
        <ProfilePage />
      </>
    ),
  },
  {
    path: '/exchange/incoming',
    element: (
      <>
        <Navbar />
        <IncomingRequestsPage />
      </>
    ),
  },
  {
    path: '/exchange/outgoing',
    element: (
      <>
        <Navbar />
        <OutgoingRequestsPage />
      </>
    ),
  },
  {
    path: '/admin',
    element: (
      <>
        <Navbar />
        <AdminPage />
      </>
    ),
  },
  {
    path: '/admin/statistics',
    element: (
      <>
        <Navbar />
        <AdminStatisticsPage />
      </>
    ),
  },
]);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}
