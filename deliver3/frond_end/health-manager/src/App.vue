<template>
  <v-app>
    <v-app-bar app color="primary" dark v-if="authStore.isAuthenticated">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Health Track</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app v-if="authStore.isAuthenticated">
      <v-list>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Dashboard" to="/"></v-list-item>
        <v-list-item prepend-icon="mdi-account" title="Account" to="/account"></v-list-item>
        <v-list-item prepend-icon="mdi-calendar" title="Appointments" to="/appointments"></v-list-item>
        <v-list-item prepend-icon="mdi-trophy" title="Challenges" to="/challenges"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
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

    return {
      authStore,
      drawer,
      logout
    }
  }
})
</script>
