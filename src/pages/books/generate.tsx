import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { bookService } from '../../services/book';
import type { BookGenerationConfig } from '../../types/book';

export function GenerateBook() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<BookGenerationConfig>({
    title: '',
    description: '',
    genre: '',
    target_audience: '',
    style: '',
    tone: '',
    length: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const book = await bookService.createBook(formData);
      await bookService.generateBook(book.id);
      navigate(`/books/${book.id}`);
    } catch (error) {
      console.error('Error generating book:', error);
      setError('Failed to generate book. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Generate New Book</h1>
      
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-md mb-6">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        {Object.entries(formData).map(([key, value]) => (
          <div key={key}>
            <label className="block text-sm font-medium text-gray-700 mb-1 capitalize">
              {key.replace('_', ' ')}
            </label>
            <input
              type="text"
              value={value}
              onChange={(e) => setFormData(prev => ({ ...prev, [key]: e.target.value }))}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500"
              required
              placeholder={`Enter ${key.replace('_', ' ').toLowerCase()}`}
            />
          </div>
        ))}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-purple-600 text-white px-6 py-3 rounded-full hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Generating...' : 'Generate Book'}
        </button>
      </form>
    </div>
  );
}