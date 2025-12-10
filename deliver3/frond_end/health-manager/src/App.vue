<template>
  <v-app>
    <v-app-bar app color="primary" dark v-if="authStore.isAuthenticated">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Health Track</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <div v-if="authStore.user" class="d-flex align-center mr-4">
        <span class="mr-2">{{ authStore.user.first_name }} {{ authStore.user.last_name }}</span>
        <v-avatar color="secondary" size="36">
          <span class="text-subtitle-1 font-weight-bold">{{ userInitials }}</span>
        </v-avatar>
      </div>

      <v-btn icon @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app v-if="authStore.isAuthenticated">
      <v-list>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Dashboard" to="/"></v-list-item>
        <v-list-item prepend-icon="mdi-heart-pulse" title="Health Metrics" to="/metrics"></v-list-item>
        <v-list-item prepend-icon="mdi-account" title="Account" to="/account"></v-list-item>
        <v-list-item prepend-icon="mdi-calendar" title="Appointments" to="/appointments"></v-list-item>
        <v-list-item prepend-icon="mdi-trophy" title="Challenges" to="/challenges"></v-list-item>
        <v-list-item prepend-icon="mdi-account-group" title="Family" to="/family"></v-list-item>
        <v-list-item prepend-icon="mdi-email-outline" title="Invitations" to="/invitations"></v-list-item>
        <v-list-item prepend-icon="mdi-account-key" title="Delegation" to="/delegation"></v-list-item>
        <v-list-item prepend-icon="mdi-file-chart" title="Reports" to="/reports"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const drawer = ref(true)

    const logout = async () => {
      await authStore.logout()
      router.push('/login')
    }

    const userInitials = computed(() => {
      if (authStore.user && authStore.user.first_name && authStore.user.last_name) {
        return `${authStore.user.first_name[0]}${authStore.user.last_name[0]}`.toUpperCase()
      }
      return 'U'
    })

    return {
      authStore,
      drawer,
      logout,
      userInitials
    }
  }
})
</script>
