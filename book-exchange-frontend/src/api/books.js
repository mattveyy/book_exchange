const BASE_URL = 'http://127.0.0.1:5000';

export async function getBooks() {
  const res = await fetch(`${BASE_URL}/books`);
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || 'Ошибка при получении книг');
  }
  return res.json();
}

export async function deleteBook(bookId) {
  const res = await fetch(`${BASE_URL}/books/${bookId}`, {
    method: 'DELETE',
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || 'Ошибка удаления книги');
  }
}