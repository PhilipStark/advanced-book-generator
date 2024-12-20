import { BookGenerationConfig, Book, GenerationProgress } from '../types/book';

class BookService {
  private baseUrl = 'http://localhost:8000';

  async createBook(config: BookGenerationConfig): Promise<Book> {
    try {
      const response = await fetch(`${this.baseUrl}/books`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating book:', error);
      throw error;
    }
  }

  async generateBook(id: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/books/${id}/generate`, {
        method: 'POST',
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error generating book:', error);
      throw error;
    }
  }

  async getBookStatus(id: number): Promise<Book> {
    try {
      const response = await fetch(`${this.baseUrl}/books/${id}/status`, {
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting book status:', error);
      throw error;
    }
  }

  subscribeToProgress(id: number, onProgress: (data: GenerationProgress) => void): () => void {
    const eventSource = new EventSource(`${this.baseUrl}/events/${id}`);
    
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onProgress(data);
      } catch (error) {
        console.error('Error parsing event data:', error);
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource error:', error);
    };

    return () => eventSource.close();
  }
}

export const bookService = new BookService();