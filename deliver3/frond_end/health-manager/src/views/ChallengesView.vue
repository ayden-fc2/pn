<template>
  <v-container>
    <h1 class="text-h4 mb-4">Challenges</h1>
    
    <v-row>
      <v-col v-for="challenge in challenges" :key="challenge.challenge_id" cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>{{ challenge.title }}</v-card-title>
          <v-card-text>
            <p>{{ challenge.description }}</p>
            <div class="mt-2">
              <v-chip v-if="challenge.joined" color="success" class="mr-2">Joined</v-chip>
              <v-chip v-else color="grey">Not Joined</v-chip>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn v-if="!challenge.joined" color="primary" @click="joinChallenge(challenge.challenge_id)">Join</v-btn>
            <v-btn v-else color="error" @click="leaveChallenge(challenge.challenge_id)">Leave</v-btn>
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
  name: 'ChallengesView',
  setup() {
    const challenges = ref<any[]>([])
    
    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const showMessage = (text: string, color = 'success') => {
      snackbarText.value = text
      snackbarColor.value = color
      snackbar.value = true
    }

    const fetchChallenges = async () => {
      try {
        const response = await api.get('/challenges')
        challenges.value = response.data
      } catch (error) {
        console.error('Error fetching challenges:', error)
      }
    }

    const joinChallenge = async (id: number) => {
      try {
        await api.post(`/challenges/${id}/join`)
        await fetchChallenges()
        showMessage('Joined challenge')
      } catch (error) {
        showMessage('Failed to join challenge', 'error')
      }
    }

    const leaveChallenge = async (id: number) => {
      try {
        await api.post(`/challenges/${id}/leave`)
        await fetchChallenges()
        showMessage('Left challenge')
      } catch (error) {
        showMessage('Failed to leave challenge', 'error')
      }
    }

    onMounted(() => {
      fetchChallenges()
    })

    return {
      challenges,
      joinChallenge,
      leaveChallenge,
      snackbar,
      snackbarText,
      snackbarColor
    }
  }
})
</script>
