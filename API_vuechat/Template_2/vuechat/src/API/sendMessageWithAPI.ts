const BASE_API_URL = "http://10.121.252.227:8000/api"; // ← Замени на свой публичный адрес (или бери из .env)

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
  // Шаг 1 — создать задачу на генерацию
  const createRes = await fetch(`${BASE_API_URL}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!createRes.ok) {
    const errText = await createRes.text();
    throw new Error(`Ошибка при создании запроса: ${errText}`);
  }

  const { task_id } = await createRes.json();
  if (!task_id) throw new Error("task_id не получен от API");

  // Шаг 2 — опрашивать задачу и ждать завершения
  return new Promise((resolve, reject) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${BASE_API_URL}/generate/${task_id}`);
        const json = await res.json();

        if (json.status === "success") {
          clearInterval(interval);
          resolve(json.response);
        } else if (json.status === "error") {
          clearInterval(interval);
          reject(json.error || "Неизвестная ошибка");
        }
      } catch (err) {
        clearInterval(interval);
        reject("Ошибка при получении результата: " + err);
      }
    }, 1000);
  });
}
