<template>
  <v-container>
    <h1 class="text-h4 mb-4">Invitations</h1>

    <v-card v-if="invitations.length === 0">
        <v-card-text>No pending invitations.</v-card-text>
    </v-card>

    <v-row v-else>
      <v-col v-for="invite in invitations" :key="invite.invitation_id" cols="12" md="6">
        <v-card :color="invite.status === 'Pending' ? undefined : 'grey-lighten-4'">
          <v-card-title>
            {{ invite.type }} Invitation
            <v-chip size="small" class="ml-2" :color="getStatusColor(invite.status)">{{ invite.status }}</v-chip>
          </v-card-title>
          <v-card-subtitle>From: {{ invite.sender_name }} {{ invite.sender_last_name }}</v-card-subtitle>
          <v-card-text>
            <div v-if="invite.type === 'Challenge'">
                Challenge: {{ invite.challenge_name }}
            </div>
            <div v-else>
                Join my family group
            </div>
          </v-card-text>
          <v-card-actions v-if="invite.status === 'Pending'">
            <v-btn color="success" @click="respond(invite.invitation_id, 'Accepted')">Accept</v-btn>
            <v-btn color="error" @click="respond(invite.invitation_id, 'Rejected')">Reject</v-btn>
          </v-card-actions>
        </v-card>
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
  name: 'InvitationsView',
  setup() {
    const invitations = ref<any[]>([])
    
    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const showMessage = (text: string, color = 'success') => {
      snackbarText.value = text
      snackbarColor.value = color
      snackbar.value = true
    }

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'Pending': return 'warning'
            case 'Accepted': return 'success'
            case 'Rejected': return 'error'
            default: return 'grey'
        }
    }

    const fetchInvitations = async () => {
      try {
        const response = await api.get('/invitations')
        invitations.value = response.data
      } catch (error) {
        console.error('Error fetching invitations:', error)
      }
    }

    const respond = async (id: number, status: string) => {
      try {
        await api.post(`/invitations/${id}/respond`, { status })
        await fetchInvitations()
        showMessage(`Invitation ${status}`)
      } catch (error: any) {
        const msg = error.response?.data?.error || 'Failed to respond'
        showMessage(msg, 'error')
      }
    }

    onMounted(() => {
      fetchInvitations()
    })

    return {
      invitations,
      respond,
      getStatusColor,
      snackbar,
      snackbarText,
      snackbarColor
    }
  }
})
</script>
