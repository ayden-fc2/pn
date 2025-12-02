<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="email"
                label="Email"
                name="login"
                prepend-icon="mdi-email"
                type="email"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                id="password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="handleLogin">Login</v-btn>
          </v-card-actions>
        </v-card>
        <v-alert v-if="error" type="error" class="mt-3">
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'LoginView',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const error = ref('')

    const handleLogin = async () => {
      if (!email.value || !password.value) {
        error.value = 'Please enter Email and Password'
        return
      }
      
      const success = await authStore.login(email.value, password.value)
      if (success) {
        router.push('/')
      } else {
        error.value = 'Invalid credentials'
      }
    }

    return {
      email,
      password,
      handleLogin,
      error
    }
  }
})
</script>
