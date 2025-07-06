from groq import Groq
client = Groq(api_key="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")  # замените на свой настоящий ключ

completion = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",
    messages=[
      {
        "role": "user",
        "content": "hello, how are you?"
      }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
