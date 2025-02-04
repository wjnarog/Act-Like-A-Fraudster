export default async function handler(req, res) {
    if (req.method === 'POST') {
      const { query } = req.body;
  
      // Forward the request to your Python backend
      const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
  
      // Send the response back to the frontend
      res.status(200).json(data);
    } else {
      res.status(405).json({ message: 'Method not allowed' });
    }
  }