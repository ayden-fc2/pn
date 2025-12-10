<template>
  <v-container>
    <h1 class="text-h4 mb-4">Dashboard</h1>
    <v-row v-if="summary">
      <!-- BMI Card -->
      <v-col cols="12" md="4">
        <v-card color="primary" dark height="100%">
          <v-card-title class="text-h5">BMI</v-card-title>
          <v-card-text class="text-h2 font-weight-bold">
            {{ summary.bmi.toFixed(1) }}
          </v-card-text>
          <v-card-subtitle>Category: {{ getBmiCategory(summary.bmi) }}</v-card-subtitle>
          <v-card-actions>
            <v-btn variant="text" @click="showUpdateMetrics = true">Update</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Invitations Card -->
      <v-col cols="12" md="4">
        <v-card color="warning" dark height="100%" to="/invitations">
          <v-card-title class="text-h5">Pending Invitations</v-card-title>
          <v-card-text class="text-h2 font-weight-bold">
            {{ summary.pending_invitations }}
          </v-card-text>
          <v-card-subtitle>Click to view details</v-card-subtitle>
        </v-card>
      </v-col>

      <!-- Stats Summary -->
      <v-col cols="12" md="4">
        <v-card height="100%">
            <v-card-title>Quick Stats</v-card-title>
            <v-list density="compact">
                <v-list-item>
                    <v-list-item-title>Active Challenges</v-list-item-title>
                    <template v-slot:append>{{ summary.active_challenges_count }}</template>
                </v-list-item>
                <v-list-item>
                    <v-list-item-title>Upcoming Appointments</v-list-item-title>
                    <template v-slot:append>{{ summary.upcoming_appointments_count }}</template>
                </v-list-item>
            </v-list>
        </v-card>
      </v-col>

      <!-- Upcoming Appointments List -->
      <v-col cols="12" md="6">
        <v-card height="100%">
          <v-card-title class="d-flex justify-space-between align-center">
            Upcoming Appointments
            <v-btn variant="text" size="small" to="/appointments">View All</v-btn>
          </v-card-title>
          <v-card-text>
            <v-list v-if="summary.upcoming_appointments.length > 0">
              <v-list-item v-for="app in summary.upcoming_appointments" :key="app.appointment_id">
                <v-list-item-title>{{ app.appointment_type }} with {{ app.provider_name }}</v-list-item-title>
                <v-list-item-subtitle>{{ new Date(app.appointment_date).toLocaleString() }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <div v-else class="text-center pa-4 text-grey">No upcoming appointments</div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Active Challenges List -->
      <v-col cols="12" md="6">
        <v-card height="100%">
          <v-card-title class="d-flex justify-space-between align-center">
            Active Challenges
            <v-btn variant="text" size="small" to="/challenges">View All</v-btn>
          </v-card-title>
          <v-card-text>
            <v-list v-if="summary.active_challenges.length > 0">
              <v-list-item v-for="chal in summary.active_challenges" :key="chal.challenge_id">
                <v-list-item-title>{{ chal.name }}</v-list-item-title>
                <v-list-item-subtitle>Goal: {{ chal.goal }}</v-list-item-subtitle>
                <template v-slot:append>
                    <v-chip size="small" color="info">{{ chal.progress_value }}</v-chip>
                </template>
              </v-list-item>
            </v-list>
            <div v-else class="text-center pa-4 text-grey">No active challenges</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-dialog v-model="showUpdateMetrics" max-width="500px">
      <v-card>
        <v-card-title>Update Health Metrics</v-card-title>
        <v-card-text>
          <v-text-field v-model="newWeight" label="Weight (kg)" type="number"></v-text-field>
          <v-text-field v-model="newHeight" label="Height (cm)" type="number"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="updateMetrics">Save</v-btn>
          <v-btn color="grey" text @click="showUpdateMetrics = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import api from '@/api/axios'

export default defineComponent({
  name: 'DashboardView',
  setup() {
    const summary = ref<any>(null)
    const showUpdateMetrics = ref(false)
    const newWeight = ref('')
    const newHeight = ref('')

    const fetchSummary = async () => {
      try {
        const response = await api.get('/summary')
        summary.value = response.data
      } catch (error) {
        console.error('Error fetching summary:', error)
      }
    }

    const updateMetrics = async () => {
      try {
        if (newWeight.value) {
          await api.post('/metrics', { type: 'Weight', value: Number(newWeight.value) })
        }
        if (newHeight.value) {
          await api.post('/metrics', { type: 'Height', value: Number(newHeight.value) })
        }
        showUpdateMetrics.value = false
        newWeight.value = ''
        newHeight.value = ''
        await fetchSummary()
      } catch (error) {
        console.error('Error updating metrics:', error)
      }
    }

    const getBmiCategory = (bmi: number) => {
      if (bmi < 18.5) return 'Underweight'
      if (bmi < 25) return 'Normal weight'
      if (bmi < 30) return 'Overweight'
      return 'Obesity'
    }

    onMounted(() => {
      fetchSummary()
    })

    return {
      summary,
      getBmiCategory,
      showUpdateMetrics,
      newWeight,
      newHeight,
      updateMetrics
    }
  }
})
</script>
