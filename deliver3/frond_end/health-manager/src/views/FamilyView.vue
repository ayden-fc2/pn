<template>
  <v-container>
    <h1 class="text-h4 mb-4">Family Group</h1>

    <v-card v-if="!familyGroup" class="mb-4">
      <v-card-title>Create Family Group</v-card-title>
      <v-card-text>
        <v-text-field v-model="newGroupName" label="Group Name"></v-text-field>
        <v-btn color="primary" @click="createGroup">Create</v-btn>
      </v-card-text>
    </v-card>

    <v-card v-else class="mb-4">
      <v-card-title>{{ familyGroup.name }}</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item v-for="member in familyGroup.members" :key="member.user_id">
            <v-list-item-title>{{ member.first_name }} {{ member.last_name }}</v-list-item-title>
            <v-list-item-subtitle>{{ member.role }} - Joined: {{ member.joined_at }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-btn color="error" @click="leaveGroup">Leave Group</v-btn>
        <v-btn color="primary" @click="showInviteDialog = true">Invite Member</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Invite Dialog -->
    <v-dialog v-model="showInviteDialog" max-width="400">
      <v-card>
        <v-card-title>Invite Family Member</v-card-title>
        <v-card-text>
          <v-text-field v-model="inviteEmail" label="Email Address"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="showInviteDialog = false">Cancel</v-btn>
          <v-btn color="primary" text @click="sendInvite">Send Invite</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
  name: 'FamilyView',
  setup() {
    const familyGroup = ref<any>(null)
    const newGroupName = ref('')
    const showInviteDialog = ref(false)
    const inviteEmail = ref('')
    
    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const showMessage = (text: string, color = 'success') => {
      snackbarText.value = text
      snackbarColor.value = color
      snackbar.value = true
    }

    const fetchFamily = async () => {
      try {
        const response = await api.get('/family')
        if (response.data && response.data.group_id) {
            familyGroup.value = response.data
        } else {
            familyGroup.value = null
        }
      } catch (error) {
        console.error('Error fetching family:', error)
      }
    }

    const createGroup = async () => {
      if (!newGroupName.value) return
      try {
        await api.post('/family', { name: newGroupName.value })
        await fetchFamily()
        showMessage('Family group created')
      } catch (error) {
        showMessage('Failed to create group', 'error')
      }
    }

    const leaveGroup = async () => {
      try {
        await api.post('/family/leave')
        familyGroup.value = null
        showMessage('Left family group')
      } catch (error) {
        showMessage('Failed to leave group', 'error')
      }
    }

    const sendInvite = async () => {
      if (!inviteEmail.value) return
      try {
        await api.post('/invitations', {
            type: 'Family',
            target_email: inviteEmail.value
        })
        showInviteDialog.value = false
        inviteEmail.value = ''
        showMessage('Invitation sent')
      } catch (error) {
        showMessage('Failed to send invitation', 'error')
      }
    }

    onMounted(() => {
      fetchFamily()
    })

    return {
      familyGroup,
      newGroupName,
      createGroup,
      leaveGroup,
      showInviteDialog,
      inviteEmail,
      sendInvite,
      snackbar,
      snackbarText,
      snackbarColor
    }
  }
})
</script>
