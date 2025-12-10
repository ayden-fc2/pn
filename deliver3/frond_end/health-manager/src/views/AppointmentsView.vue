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
            <v-col cols="12" md="6">
              <v-text-field v-model="newAppointment.description" label="Type (e.g. Checkup)"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="newAppointment.memo" label="Memo (Optional)"></v-text-field>
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
            <th class="text-left">Type</th>
            <th class="text-left">Memo</th>
            <th class="text-left">Status</th>
            <th class="text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="apt in appointments" :key="apt.appointment_id">
            <td>{{ apt.date }}</td>
            <td>{{ apt.time }}</td>
            <td>{{ apt.provider_name }}</td>
            <td>{{ apt.description }}</td>
            <td>{{ apt.memo }}</td>
            <td>{{ apt.status }}</td>
            <td>
              <v-btn 
                v-if="apt.status !== 'Cancelled'"
                icon="mdi-cancel" 
                size="small" 
                color="error" 
                variant="text" 
                @click="openCancelDialog(apt.appointment_id)"
              ></v-btn>
            </td>
          </tr>
          <tr v-if="appointments.length === 0">
            <td colspan="7" class="text-center">No appointments found</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <!-- Cancel Dialog -->
    <v-dialog v-model="showCancelDialog" max-width="400">
      <v-card>
        <v-card-title>Cancel Appointment</v-card-title>
        <v-card-text>
          <v-text-field v-model="cancelReason" label="Reason for cancellation"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="showCancelDialog = false">Close</v-btn>
          <v-btn color="error" text @click="confirmCancel">Confirm Cancel</v-btn>
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
  name: 'AppointmentsView',
  setup() {
    const appointments = ref<any[]>([])
    const allProviders = ref<any[]>([])
    const newAppointment = ref({
      date: '',
      time: '',
      provider_id: null,
      description: '',
      memo: ''
    })
    
    const showCancelDialog = ref(false)
    const cancelReason = ref('')
    const selectedAppointmentId = ref<number | null>(null)

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
          description: newAppointment.value.description,
          memo: newAppointment.value.memo
        })
        newAppointment.value = { date: '', time: '', provider_id: null, description: '', memo: '' }
        await fetchAppointments()
        showMessage('Appointment scheduled')
      } catch (error) {
        showMessage('Failed to schedule appointment', 'error')
      }
    }

    const openCancelDialog = (id: number) => {
      selectedAppointmentId.value = id
      cancelReason.value = ''
      showCancelDialog.value = true
    }

    const confirmCancel = async () => {
      if (!selectedAppointmentId.value) return
      try {
        await api.delete(`/appointments/${selectedAppointmentId.value}`, {
          data: { reason: cancelReason.value }
        })
        await fetchAppointments()
        showMessage('Appointment cancelled')
        showCancelDialog.value = false
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
      openCancelDialog,
      confirmCancel,
      showCancelDialog,
      cancelReason,
      snackbar,
      snackbarText,
      snackbarColor
    }
  }
})
</script>
