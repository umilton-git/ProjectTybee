<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApi, type SessionPreset } from '../composables/useApi'
import { useSession } from '../composables/useSession'

const router = useRouter()
const api = useApi()
const session = useSession()

const presets = ref<SessionPreset[]>([])
const selectedPreset = ref<SessionPreset | null>(null)
const loading = ref(true)
const error = ref('')
const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)

// Fetch presets when component mounts
onMounted(async () => {
  try {
    presets.value = await api.getPresets()
  } catch (e) {
    error.value = 'Failed to load presets. Is the backend running?'
  } finally {
    loading.value = false
  }
})

function selectPreset(preset: SessionPreset) {
  selectedPreset.value = preset
}

async function startSession() {
  if (!selectedPreset.value) return
  
  await session.startSession(selectedPreset.value)
  router.push('/session')
}

// Format duration for display (30 -> "30s", 60 -> "1 min", 300 -> "5 min")
function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`
  return `${seconds / 60} min`
}

// Upload functions
function triggerUpload() {
  fileInput.value?.click()
}

async function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  uploading.value = true
  try {
    await api.uploadImage(file)
    alert('Image uploaded successfully!')
  } catch (e) {
    alert('Failed to upload image')
  } finally {
    uploading.value = false
    target.value = '' // Reset input
  }
}
</script>

<template>
  <div class="setup">
    <!-- Upload Button -->
    <button class="upload-btn" @click="triggerUpload">
      Upload
    </button>
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleFileUpload"
    />

    <h1>Tybee</h1>
    <p>Gesture Drawing Practice</p>

    <div v-if="loading">Loading presets...</div>
    
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else>
      <h2>Select a Session</h2>
      
      <div class="presets">
        <button
          v-for="preset in presets"
          :key="preset.id"
          :class="['preset-btn', { selected: selectedPreset?.id === preset.id }]"
          @click="selectPreset(preset)"
        >
          <strong>{{ preset.name }}</strong>
          <span>{{ preset.image_count }} images × {{ formatDuration(preset.duration_seconds) }}</span>
        </button>
      </div>

      <button
        class="start-btn"
        :disabled="!selectedPreset"
        @click="startSession"
      >
        Start Session
      </button>
    </div>
  </div>
</template>

<style scoped>
.setup {
  position: relative;
  text-align: center;
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.upload-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
}

.upload-btn:hover {
  background: #0056b3;
}

.presets {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 2rem 0;
}

.preset-btn {
  padding: 1rem;
  border: 2px solid #ccc;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.preset-btn:hover {
  border-color: #666;
}

.preset-btn.selected {
  border-color: #007bff;
  background: #e7f1ff;
}

.start-btn {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.start-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  color: red;
}
</style>