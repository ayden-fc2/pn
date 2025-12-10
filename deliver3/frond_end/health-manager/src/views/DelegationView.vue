<template>
  <v-container>
    <h1 class="text-h4 mb-4">Delegations</h1>

    <v-row>
        <v-col cols="12" md="6">
            <v-card class="mb-4">
                <v-card-title>My Dependents (I am Guardian)</v-card-title>
                <v-card-text>
                    <v-list>
                        <v-list-item v-for="dep in dependents" :key="dep.user_id">
                            <v-list-item-title>{{ dep.first_name }} {{ dep.last_name }}</v-list-item-title>
                            <template v-slot:append>
                                <v-btn icon="mdi-delete" size="small" color="error" variant="text" @click="removeDependent(dep.user_id)"></v-btn>
                            </template>
                        </v-list-item>
                        <v-list-item v-if="dependents.length === 0">No dependents</v-list-item>
                    </v-list>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" @click="showAddDialog = true">Add Dependent</v-btn>
                </v-card-actions>
            </v-card>
        </v-col>

        <v-col cols="12" md="6">
            <v-card>
                <v-card-title>My Guardians</v-card-title>
                <v-card-text>
                    <v-list>
                        <v-list-item v-for="g in guardians" :key="g.user_id">
                            <v-list-item-title>{{ g.first_name }} {{ g.last_name }}</v-list-item-title>
                            <template v-slot:append>
                                <v-btn icon="mdi-delete" size="small" color="error" variant="text" @click="removeGuardian(g.user_id)"></v-btn>
                            </template>
                        </v-list-item>
                        <v-list-item v-if="guardians.length === 0">No guardians</v-list-item>
                    </v-list>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>

    <!-- Add Dependent Dialog -->
    <v-dialog v-model="showAddDialog" max-width="400">
      <v-card>
        <v-card-title>Add Dependent</v-card-title>
        <v-card-text>
          <v-autocomplete
            v-model="dependentId"
            :items="users"
            item-title="fullName"
            item-value="user_id"
            label="Select Dependent"
          ></v-autocomplete>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="showAddDialog = false">Cancel</v-btn>
          <v-btn color="primary" text @click="addDependent">Add</v-btn>
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
  name: 'DelegationView',
  setup() {
    const dependents = ref<any[]>([])
    const guardians = ref<any[]>([])
    const users = ref<any[]>([])
    const showAddDialog = ref(false)
    const dependentId = ref(null)
    
    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const showMessage = (text: string, color = 'success') => {
      snackbarText.value = text
      snackbarColor.value = color
      snackbar.value = true
    }

    const fetchDelegations = async () => {
      try {
        const response = await api.get('/delegation')
        dependents.value = response.data.dependents
        guardians.value = response.data.guardians
      } catch (error) {
        console.error('Error fetching delegations:', error)
      }
    }

    const fetchUsers = async () => {
      try {
        const response = await api.get('/account/users')
        users.value = response.data.map((u: any) => ({
            ...u,
            fullName: `${u.first_name} ${u.last_name} (ID: ${u.user_id})`
        }))
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    }

    const addDependent = async () => {
      if (!dependentId.value) return
      try {
        await api.post('/delegation/add', { dependent_id: dependentId.value })
        await fetchDelegations()
        showAddDialog.value = false
        dependentId.value = null
        showMessage('Dependent added')
      } catch (error) {
        showMessage('Failed to add dependent', 'error')
      }
    }

    const removeDependent = async (id: number) => {
      try {
        await api.post('/delegation/remove', { dependent_id: id })
        await fetchDelegations()
        showMessage('Dependent removed')
      } catch (error) {
        showMessage('Failed to remove dependent', 'error')
      }
    }

    const removeGuardian = async (id: number) => {
      try {
        await api.post('/delegation/remove', { guardian_id: id })
        await fetchDelegations()
        showMessage('Guardian removed')
      } catch (error) {
        showMessage('Failed to remove guardian', 'error')
      }
    }

    onMounted(() => {
      fetchDelegations()
      fetchUsers()
    })

    return {
      dependents,
      guardians,
      users,
      showAddDialog,
      dependentId,
      addDependent,
      removeDependent,
      removeGuardian,
      snackbar,
      snackbarText,
      snackbarColor
    }
  }
})
</script>
