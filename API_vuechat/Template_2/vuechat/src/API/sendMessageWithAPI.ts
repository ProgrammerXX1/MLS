export async function generateTextRequest(payload: {
  user_id: string;
  api_key: string;
  model: string;
  messages: { role: string; content: string }[];
  temperature: number;
  max_tokens: number;
  response_format: string;
  moderation: boolean;
  top_p: number;
  seed?: string;
  stop?: string;
}): Promise<string> {
  const response = await fetch('http://localhost:8000/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  const taskId = data.task_id;
  if (!taskId) throw new Error('Task ID not returned');

  return new Promise((resolve, reject) => {
    const interval = setInterval(async () => {
      const result = await fetch(`http://localhost:8000/api/generate/${taskId}`);
      const json = await result.json();

      if (json.status === 'success') {
        clearInterval(interval);
        resolve(json.response);
      } else if (json.status === 'error') {
        clearInterval(interval);
        reject(json.error || 'Unknown error');
      }
    }, 1000);
  });
}
