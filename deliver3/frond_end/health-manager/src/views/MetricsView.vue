<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Health Metrics</h1>
      <v-btn color="primary" @click="showAddDialog = true">Add Metric</v-btn>
    </div>

    <v-card>
      <v-table>
        <thead>
          <tr>
            <th class="text-left">Type</th>
            <th class="text-left">Value</th>
            <th class="text-left">Unit</th>
            <th class="text-left">Date</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="metric in metrics" :key="metric.metric_id">
            <td>{{ metric.metric_type }}</td>
            <td>{{ metric.value }}</td>
            <td>{{ metric.unit }}</td>
            <td>{{ new Date(metric.recorded_date).toLocaleString() }}</td>
            <td class="text-right">
              <v-btn icon="mdi-delete" size="small" color="error" variant="text" @click="deleteMetric(metric.metric_id)"></v-btn>
            </td>
          </tr>
          <tr v-if="metrics.length === 0">
            <td colspan="5" class="text-center pa-4 text-grey">No metrics recorded</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <!-- Add Metric Dialog -->
    <v-dialog v-model="showAddDialog" max-width="500px">
      <v-card>
        <v-card-title>Add Health Metric</v-card-title>
        <v-card-text>
          <v-select
            v-model="selectedMetricType"
            :items="metricTypes"
            label="Metric Type"
            @update:model-value="updateUnit"
          ></v-select>
          <v-text-field v-model="metricValue" label="Value" type="number"></v-text-field>
          <v-text-field v-model="metricUnit" label="Unit"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="addMetric">Add</v-btn>
          <v-btn color="grey" text @click="showAddDialog = false">Cancel</v-btn>
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
  name: 'MetricsView',
  setup() {
    const metrics = ref<any[]>([])
    const showAddDialog = ref(false)
    
    const metricTypes = ['Weight', 'Height', 'Blood Pressure', 'Steps', 'Heart Rate', 'Sleep', 'Run Distance']
    const selectedMetricType = ref('Weight')
    const metricValue = ref('')
    const metricUnit = ref('kg')

    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const showMessage = (text: string, color = 'success') => {
      snackbarText.value = text
      snackbarColor.value = color
      snackbar.value = true
    }

    const fetchMetrics = async () => {
      try {
        const response = await api.get('/metrics/history')
        metrics.value = response.data
      } catch (error) {
        console.error('Error fetching metrics:', error)
      }
    }

    const updateUnit = (type: string) => {
      switch (type) {
        case 'Weight': metricUnit.value = 'kg'; break;
        case 'Height': metricUnit.value = 'cm'; break;
        case 'Blood Pressure': metricUnit.value = 'mmHg'; break;
        case 'Steps': metricUnit.value = 'count'; break;
        case 'Heart Rate': metricUnit.value = 'bpm'; break;
        case 'Sleep': metricUnit.value = 'hours'; break;
        case 'Run Distance': metricUnit.value = 'km'; break;
        default: metricUnit.value = '';
      }
    }

    const addMetric = async () => {
      try {
        if (selectedMetricType.value && metricValue.value) {
          await api.post('/metrics', { 
            type: selectedMetricType.value, 
            value: Number(metricValue.value),
            unit: metricUnit.value
          })
          
          showAddDialog.value = false
          metricValue.value = ''
          await fetchMetrics()
          showMessage('Metric added successfully')
        }
      } catch (error) {
        console.error('Error adding metric:', error)
        showMessage('Failed to add metric', 'error')
      }
    }

    const deleteMetric = async (id: number) => {
      if (!confirm('Are you sure you want to delete this record?')) return
      
      try {
        await api.delete(`/metrics/${id}`)
        await fetchMetrics()
        showMessage('Metric deleted')
      } catch (error) {
        console.error('Error deleting metric:', error)
        showMessage('Failed to delete metric', 'error')
      }
    }

    onMounted(() => {
      fetchMetrics()
    })

    return {
      metrics,
      showAddDialog,
      metricTypes,
      selectedMetricType,
      metricValue,
      metricUnit,
      updateUnit,
      addMetric,
      deleteMetric,
      snackbar,
      snackbarText,
      snackbarColor
    }
  }
})
</script>
