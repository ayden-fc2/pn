<template>
  <v-container>
    <h1 class="text-h4 mb-4">Dashboard</h1>
    <v-row v-if="summary">
      <v-col cols="12" md="4">
        <v-card color="primary" dark>
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
      <v-col cols="12" md="4">
        <v-card color="success" dark>
          <v-card-title class="text-h5">Active Challenges</v-card-title>
          <v-card-text class="text-h2 font-weight-bold">
            {{ summary.active_challenges }}
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card color="info" dark>
          <v-card-title class="text-h5">Upcoming Appointments</v-card-title>
          <v-card-text class="text-h2 font-weight-bold">
            {{ summary.upcoming_appointments }}
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
