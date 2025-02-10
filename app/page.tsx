'use client';
import { useState } from 'react';

export default function Home() {
  const [word, setWord] = useState(null);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');

  const getQuery = async () => {
    if (!query.trim()) {
      alert('Please enter a query.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setWord(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    button: {
      padding: '10px 20px',
      fontSize: '16px',
      backgroundColor: '#0070f3',
      color: '#fff',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
    },
    numberText: {
      fontSize: '20px',
      marginTop: '20px',
    },
    input: {
      padding: '10px',
      fontSize: '16px',
      marginRight: '10px',
      borderRadius: '5px',
      border: '1px solid #ccc',
    },
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Response Generator</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter a query (e.g., pizza)"
        style={styles.input}
      />
      <button onClick={getQuery} style={styles.button} disabled={loading}>
        {loading ? 'Loading...' : 'Generate Word'}
      </button>
      {word !== null && (
        <p style={styles.numberText}>
          Your word is: {word.color} (Temperature: {word.temperature})
        </p>
      )}
    </div>
  );
}