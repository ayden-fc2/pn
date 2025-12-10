<template>
  <v-container>
    <h1 class="text-h4 mb-4">Account Management</h1>
    
    <v-row v-if="account">
      <!-- Profile Info -->
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-card-title>Profile Information</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="updateProfile">
              <v-text-field v-model="account.user.first_name" label="First Name"></v-text-field>
              <v-text-field v-model="account.user.last_name" label="Last Name"></v-text-field>
              <v-text-field v-model="account.user.address" label="Address"></v-text-field>
              <v-btn color="primary" type="submit">Update Profile</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Emails -->
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-card-title>Emails</v-card-title>
          <v-list>
            <v-list-item v-for="email in account.emails" :key="email.email_address">
              <v-list-item-title>
                {{ email.email_address }}
                <v-chip size="x-small" :color="email.is_verified ? 'success' : 'warning'" class="ml-2">
                  {{ email.is_verified ? 'Verified' : 'Unverified' }}
                </v-chip>
              </v-list-item-title>
              <template v-slot:append>
                <v-btn icon="mdi-delete" size="small" color="error" variant="text" @click="deleteEmail(email.email_address)"></v-btn>
              </template>
            </v-list-item>
          </v-list>
          <v-card-actions>
            <v-text-field v-model="newEmail" label="Add Email" density="compact" hide-details class="mr-2"></v-text-field>
            <v-btn color="success" @click="addEmail">Add</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Phones -->
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-card-title>Phone Numbers</v-card-title>
          <v-list>
            <v-list-item v-for="phone in account.phones" :key="phone.phone_number">
              <v-list-item-title>
                {{ phone.phone_number }}
                <v-chip size="x-small" :color="phone.is_verified ? 'success' : 'warning'" class="ml-2">
                  {{ phone.is_verified ? 'Verified' : 'Unverified' }}
                </v-chip>
              </v-list-item-title>
              <template v-slot:append>
                <v-btn icon="mdi-delete" size="small" color="error" variant="text" @click="deletePhone(phone.phone_number)"></v-btn>
              </template>
            </v-list-item>
          </v-list>
          <v-card-actions>
            <v-text-field v-model="newPhone" label="Add Phone" density="compact" hide-details class="mr-2"></v-text-field>
            <v-btn color="success" @click="addPhone">Add</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Providers -->
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-card-title>Linked Providers</v-card-title>
          <v-list>
            <v-list-item v-for="provider in account.providers" :key="provider.provider_id">
              <v-list-item-title>
                {{ provider.provider_name }}
                <v-chip size="x-small" :color="provider.is_verified ? 'success' : 'warning'" class="ml-2">
                  {{ provider.is_verified ? 'Verified' : 'Unverified' }}
                </v-chip>
              </v-list-item-title>
              <v-list-item-subtitle>{{ provider.specialty }}</v-list-item-subtitle>
              <template v-slot:append>
                <v-btn icon="mdi-link-off" size="small" color="error" variant="text" @click="unlinkProvider(provider.provider_id)"></v-btn>
              </template>
            </v-list-item>
          </v-list>
          <v-card-actions>
            <v-select
              v-model="newProviderId"
              :items="allProviders"
              item-title="provider_name"
              item-value="provider_id"
              label="Select Provider"
              density="compact"
              hide-details
              class="mr-2"
            ></v-select>
            <v-btn color="success" @click="linkProvider">Link</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" :color="snackbarColor">
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import api from '@/api/axios'

export default defineComponent({
  name: 'AccountView',
  setup() {
    const account = ref<any>(null)
    const allProviders = ref<any[]>([])
    const newEmail = ref('')
    const newPhone = ref('')
    const newProviderId = ref(null)
    
    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const showMessage = (text: string, color = 'success') => {
      snackbarText.value = text
      snackbarColor.value = color
      snackbar.value = true
    }

    const fetchAccount = async () => {
      try {
        const response = await api.get('/account')
        account.value = response.data
      } catch (error) {
        console.error('Error fetching account:', error)
      }
    }

    const fetchAllProviders = async () => {
      try {
        const response = await api.get('/account/providers')
        allProviders.value = response.data
      } catch (error) {
        console.error('Error fetching providers:', error)
      }
    }

    const updateProfile = async () => {
      try {
        await api.put('/account', {
          first_name: account.value.user.first_name,
          last_name: account.value.user.last_name,
          address: account.value.user.address
        })
        showMessage('Profile updated successfully')
      } catch (error) {
        showMessage('Failed to update profile', 'error')
      }
    }

    const addEmail = async () => {
      if (!newEmail.value) return
      try {
        await api.post('/account/email', { email: newEmail.value })
        newEmail.value = ''
        await fetchAccount()
        showMessage('Email added')
      } catch (error) {
        showMessage('Failed to add email', 'error')
      }
    }

    const deleteEmail = async (email: string) => {
      try {
        await api.delete('/account/email', { data: { email } })
        await fetchAccount()
        showMessage('Email deleted')
      } catch (error) {
        showMessage('Failed to delete email', 'error')
      }
    }

    const addPhone = async () => {
      if (!newPhone.value) return
      try {
        await api.post('/account/phone', { phone: newPhone.value })
        newPhone.value = ''
        await fetchAccount()
        showMessage('Phone added')
      } catch (error) {
        showMessage('Failed to add phone', 'error')
      }
    }

    const deletePhone = async (phone: string) => {
      try {
        await api.delete('/account/phone', { data: { phone } })
        await fetchAccount()
        showMessage('Phone deleted')
      } catch (error) {
        showMessage('Failed to delete phone', 'error')
      }
    }

    const linkProvider = async () => {
      if (!newProviderId.value) return
      try {
        await api.post('/account/provider', { provider_id: Number(newProviderId.value) })
        newProviderId.value = null
        await fetchAccount()
        showMessage('Provider linked')
      } catch (error) {
        showMessage('Failed to link provider', 'error')
      }
    }

    const unlinkProvider = async (providerId: number) => {
      try {
        await api.delete('/account/provider', { data: { provider_id: providerId } })
        await fetchAccount()
        showMessage('Provider unlinked')
      } catch (error) {
        showMessage('Failed to unlink provider', 'error')
      }
    }

    onMounted(() => {
      fetchAccount()
      fetchAllProviders()
    })

    return {
      account,
      allProviders,
      newEmail,
      newPhone,
      newProviderId,
      updateProfile,
      addEmail,
      deleteEmail,
      addPhone,
      deletePhone,
      linkProvider,
      unlinkProvider,
      snackbar,
      snackbarText,
      snackbarColor
    }
  }
})
</script>
