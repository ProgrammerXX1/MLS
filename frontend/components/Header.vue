<template>
  <header class="w-full bg-[#1e1e1e] h-12 px-6 flex items-center justify-between border-b border-neutral-800 relative">
    <!-- Logo -->
    <div class="flex items-center font-semibold text-xl tracking-tight">
      <span class="text-white">Au</span><span class="text-red-700">rus</span>
    </div>

    <!-- Right side -->
    <div class="flex items-center space-x-8 relative">
      <!-- Navigation -->
      <nav class="flex items-center space-x-10 text-sm text-neutral-300">
        <NuxtLink to="/" class="hover:text-red-500" :class="{ 'text-orange-500': route.path === '/' }">Playground</NuxtLink>
        <NuxtLink to="/api_keys" class="hover:text-red-500" :class="{ 'text-orange-500': route.path === '/api_keys' }">API Keys</NuxtLink>
        <NuxtLink to="/dashboard/metrics" class="hover:text-red-500" :class="{ 'text-orange-500': route.path === '/dashboard/metrics' }">Dashboard</NuxtLink>
        <NuxtLink to="/in_dev" class="hover:text-red-500" :class="{ 'text-orange-500': route.path === '/in_dev' }">Docs</NuxtLink>
      </nav>

      <!-- Settings Icon & Dropdown -->
      <div class="relative" @mouseenter="isSettingsOpen = true" @mouseleave="isSettingsOpen = false">
        <Icon icon="lucide:settings" class="text-neutral-400 hover:text-white text-lg cursor-pointer" />
        <transition name="fade">
          <div
            v-if="isSettingsOpen"
            class="absolute right-0 mt-2 w-56 bg-[#1a1a1a] border border-neutral-800 rounded-md shadow-lg z-50 text-sm text-white"
          >
            <div class="px-4 py-2 hover:bg-[#2a2a2a] cursor-pointer">Organization</div>
            <div class="px-4 py-2 hover:bg-[#2a2a2a] cursor-pointer">Billing</div>
            <div class="px-4 py-2 hover:bg-[#2a2a2a] cursor-pointer">Team</div>
            <div class="px-4 py-2 hover:bg-[#2a2a2a] cursor-pointer">Profile</div>
            <div class="px-4 py-2 hover:bg-[#2a2a2a] cursor-pointer">Model Terms</div>
          </div>
        </transition>
      </div>

      <!-- Profile Dropdown -->
      <div class="relative" @mouseenter="isProfileOpen = true" @mouseleave="isProfileOpen = false">
        <div class="flex items-center space-x-4 px-6 py-1 border border-neutral-600 rounded-full bg-[#2c2c2c] cursor-pointer">
          <div class="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold">Б</div>
          <span class="text-sm text-white font-medium">Personal</span>
        </div>
        <transition name="fade">
          <div
            v-if="isProfileOpen"
            class="absolute right-0 mt-2 w-72 bg-[#1a1a1a] border border-neutral-800 rounded-md shadow-lg z-50 text-sm text-white"
          >
            <div class="px-4 py-3 border-b border-neutral-800">
              <div class="font-semibold text-white truncate">{{ userStore.username || 'Гость' }}</div>
              <div class="text-neutral-400 text-xs truncate">{{ userStore.username }}@gmail.com</div>
            </div>
            <div class="px-4 py-2 border-b border-neutral-800 hover:bg-[#2a2a2a] cursor-pointer text-red-500 font-medium">⚡ Upgrade</div>
            <div class="px-4 py-2 border-b border-neutral-800 text-white space-y-1">
              <div class="py-1 flex justify-between items-center hover:text-red-500 cursor-pointer" :class="{ 'text-red-500': selected === 'personal' }" @click="selected = 'personal'">
                <span>Account : Personal</span>
                <span v-if="selected === 'personal'" class="text-xs text-neutral-400">✔</span>
              </div>
              <div class="py-1 hover:text-red-500 cursor-pointer">Status</div>
              <div class="py-1 hover:text-red-500 cursor-pointer">Chat with us</div>
              <div class="py-1 hover:text-red-500 cursor-pointer">Provide Feedback</div>
            </div>
            <div class="px-4 py-2 hover:bg-[#2a2a2a] cursor-pointer text-white" @click="handleLogout">Log out</div>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useUserStore } from '~/stores/user'
const userStore = useUserStore()
const route = useRoute()
const isProfileOpen = ref(false)
const isSettingsOpen = ref(false)
const selected = ref<'personal' | null>('personal')

const handleLogout = () => {
  userStore.logout()
  navigateTo('/login')
}

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
