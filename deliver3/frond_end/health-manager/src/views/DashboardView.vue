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
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import api from '@/api/axios'

export default defineComponent({
  name: 'DashboardView',
  setup() {
    const summary = ref<any>(null)

    const fetchSummary = async () => {
      try {
        const response = await api.get('/summary')
        summary.value = response.data
      } catch (error) {
        console.error('Error fetching summary:', error)
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
      getBmiCategory
    }
  }
})
</script>
