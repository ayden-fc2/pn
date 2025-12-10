<template>
  <v-container>
    <h1 class="text-h4 mb-4">Monthly Health Reports</h1>

    <v-card v-if="reports.length === 0">
        <v-card-text>No reports available.</v-card-text>
    </v-card>

    <v-row v-else>
      <v-col v-for="report in reports" :key="report.report_id" cols="12" md="6">
        <v-card>
          <v-card-title>{{ report.month }} Report</v-card-title>
          <v-card-subtitle>Generated at: {{ new Date(report.generated_at).toLocaleString() }}</v-card-subtitle>
          <v-card-text>
            <div class="text-h6 mb-2">Summary</div>
            <p>{{ report.summary }}</p>
            <v-divider class="my-3"></v-divider>
            <div class="d-flex align-center">
                <v-icon color="primary" class="mr-2">mdi-walk</v-icon>
                <span class="text-body-1">Total Steps: <strong>{{ report.steps_total }}</strong></span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import api from '@/api/axios'

export default defineComponent({
  name: 'ReportsView',
  setup() {
    const reports = ref<any[]>([])

    const fetchReports = async () => {
      try {
        const response = await api.get('/reports')
        reports.value = response.data
      } catch (error) {
        console.error('Error fetching reports:', error)
      }
    }

    onMounted(() => {
      fetchReports()
    })

    return {
      reports
    }
  }
})
</script>
