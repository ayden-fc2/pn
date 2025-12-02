<template>
  <v-container>
    <h1 class="text-h4 mb-4">Appointments</h1>
    
    <v-card class="mb-4">
      <v-card-title>Schedule New Appointment</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="scheduleAppointment">
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field v-model="newAppointment.date" label="Date (YYYY-MM-DD)" type="date"></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="newAppointment.time"
                :items="timeSlots"
                label="Time"
              ></v-select>
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="newAppointment.provider_id"
                :items="allProviders"
                item-title="provider_name"
                item-value="provider_id"
                label="Select Provider"
              ></v-select>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="newAppointment.description" label="Description"></v-text-field>
            </v-col>
          </v-row>
          <v-btn color="primary" type="submit">Schedule</v-btn>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>Upcoming Appointments</v-card-title>
      <v-table>
        <thead>
          <tr>
            <th class="text-left">Date</th>
            <th class="text-left">Time</th>
            <th class="text-left">Provider</th>
            <th class="text-left">Description</th>
            <th class="text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="apt in appointments" :key="apt.appointment_id">
            <td>{{ apt.date }}</td>
            <td>{{ apt.time }}</td>
            <td>{{ apt.provider_name }}</td>
            <td>{{ apt.description }}</td>
            <td>
              <v-btn icon="mdi-delete" size="small" color="error" variant="text" @click="cancelAppointment(apt.appointment_id)"></v-btn>
            </td>
          </tr>
          <tr v-if="appointments.length === 0">
            <td colspan="5" class="text-center">No appointments found</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

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
  name: 'AppointmentsView',
  setup() {
    const appointments = ref<any[]>([])
    const allProviders = ref<any[]>([])
    const newAppointment = ref({
      date: '',
      time: '',
      provider_id: null,
      description: ''
    })

    const timeSlots = [
      '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
      '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
      '16:00', '16:30', '17:00'
    ]

    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const showMessage = (text: string, color = 'success') => {
      snackbarText.value = text
      snackbarColor.value = color
      snackbar.value = true
    }

    const fetchAppointments = async () => {
      try {
        const response = await api.get('/appointments')
        appointments.value = response.data
      } catch (error) {
        console.error('Error fetching appointments:', error)
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

    const scheduleAppointment = async () => {
      if (!newAppointment.value.date || !newAppointment.value.time || !newAppointment.value.provider_id) {
        showMessage('Please fill in all required fields', 'error')
        return
      }
      try {
        await api.post('/appointments', {
          date: newAppointment.value.date,
          time: newAppointment.value.time,
          provider_id: Number(newAppointment.value.provider_id),
          description: newAppointment.value.description
        })
        newAppointment.value = { date: '', time: '', provider_id: null, description: '' }
        await fetchAppointments()
        showMessage('Appointment scheduled')
      } catch (error) {
        showMessage('Failed to schedule appointment', 'error')
      }
    }

    const cancelAppointment = async (id: number) => {
      try {
        await api.delete(`/appointments/${id}`)
        await fetchAppointments()
        showMessage('Appointment cancelled')
      } catch (error) {
        showMessage('Failed to cancel appointment', 'error')
      }
    }

    onMounted(() => {
      fetchAppointments()
      fetchAllProviders()
    })

    return {
      appointments,
      allProviders,
      newAppointment,
      timeSlots,
      scheduleAppointment,
      cancelAppointment,
      snackbar,
      snackbarText,
      snackbarColor
    }
  }
})
</script>
