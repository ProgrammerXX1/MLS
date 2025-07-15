<template>
  <div class="flex flex-col h-full p-4 overflow-auto text-sm text-white">
    <pre class="bg-[#1a1a1a] border border-neutral-700 rounded-md p-4 whitespace-pre-wrap overflow-y-auto max-h-full"><code><span class="text-purple-400">from</span> <span class="text-pink-400">TTC</span> <span class="text-purple-400">import</span> TTC

client = TTC()
completion = client.chat.completions.create(
    model=<span class="text-green-400">"{{ currentCode }}"</span>,
    messages=
    [<span v-for="(msg, index) in messages" :key="msg.id">
        {
        <span class="text-green-400">"role"</span>: <span class="text-green-400">"{{ msg.role }}"</span>,
        <span class="text-green-400">"content"</span>: <span class="text-green-400">"{{ msg.content.replace(/\"/g, '\\\"') }}"</span>
        }<span v-if="index !== messages.length - 1">,</span></span>
    ],
    temperature=<span class="text-green-400">0.6</span>,
    max_completion_tokens=<span class="text-green-400">4096</span>,
    top_p=<span class="text-green-400">0.95</span>,
    stream=<span class="text-blue-400">True</span>,
    stop=<span class="text-blue-400">None</span>,
)

<span class="text-purple-400">for</span> chunk <span class="text-purple-400">in</span> completion:
    <span class="text-pink-400">print</span>(chunk.choices[0].delta.content <span class="text-purple-400">or</span> <span class="text-green-400">""</span>, end=<span class="text-green-400">""</span>)</code></pre>
  </div>
</template>

<script setup lang="ts">
import { inject, toRef } from 'vue'
import type { Ref } from 'vue'

import { watch, ref } from 'vue'

const props = defineProps<{
  model: string
}>()

const currentCode = ref(generateCodeForModel(props.model)) // ✅ тут


// следим за изменением модели
watch(() => props.model, (newModel) => {
  console.log('[CodePanel] Selected model changed:', newModel)
  currentCode.value = generateCodeForModel(newModel)
})

// функция, генерирующая код (можно кастомизировать под свои модели)
function generateCodeForModel(model: string) {
  return `${model}`
}

const injected = inject<Ref<{ id: number; role: string; content: string }[]>>('chatMessages')
const messages = toRef(injected!)
</script>

<style scoped>
pre {
  font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
  line-height: 1.5;
}
.text-green-400 {
  color: #4ade80;
}
.text-green-400 {
  color: #f97316;
}
.text-purple-400 {
  color: #c084fc;
}
.text-pink-400 {
  color: #f472b6;
}
.text-blue-400 {
  color: #60a5fa;
}
</style>
