<script setup lang="ts">
import { watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSession } from '../composables/useSession'

const router = useRouter()
const session = useSession()

// Redirect to setup if no active session
if (!session.isSessionActive.value) {
  router.push('/')
}

// Watch for timer hitting zero - advance to next image
watch(
  () => session.remainingSeconds.value,
  (newValue, oldValue) => {
    if (newValue === 0 && oldValue > 0 && session.isSessionActive.value) {
      session.nextImage()
    }
  }
)

// Cleanup timer when leaving
onUnmounted(() => {
  session.reset()
})

function togglePause() {
  if (session.isRunning.value) {
    session.pause()
  } else {
    session.resume()
  }
}

function returnToSetup() {
  session.reset()
  router.push('/')
}
</script>

<template>
  <div class="session">
    <!-- Session Complete Screen -->
    <div v-if="session.isSessionComplete.value" class="complete">
      <h1>Session Complete!</h1>
      <p>Great practice session!</p>
      <button @click="returnToSetup">Back to Setup</button>
    </div>

    <!-- Active Session -->
    <div v-else class="active-session">
      <!-- Progress -->
      <div class="progress-info">
        {{ session.sessionProgress.value }}
      </div>

      <!-- Timer -->
      <div class="timer">
        {{ session.displayTime.value }}
      </div>

      <!-- Progress Bar -->
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ width: session.progress.value + '%' }"
        ></div>
      </div>

      <!-- Image -->
      <div class="image-container">
        <img 
          v-if="session.currentImageUrl.value"
          :src="session.currentImageUrl.value" 
          alt="Reference image"
        />
      </div>

      <!-- Controls -->
      <div class="controls">
        <button @click="togglePause">
          {{ session.isRunning.value ? 'Pause' : 'Resume' }}
        </button>
        <button @click="session.skip">Skip</button>
        <button @click="returnToSetup">End Session</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.session {
  text-align: center;
  padding: 1rem;
  max-width: 1000px;
  margin: 0 auto;
}

.progress-info {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.timer {
  font-size: 3rem;
  font-weight: bold;
  font-family: monospace;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #eee;
  border-radius: 4px;
  margin: 1rem 0;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #007bff;
  transition: width 1s linear;
}

.image-container {
  width: 100%;
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
  margin: 1rem 0;
}

.image-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.controls button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background: #007bff;
  color: white;
}

.controls button:hover {
  background: #0056b3;
}

.complete {
  padding: 4rem;
}

.complete button {
  margin-top: 2rem;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>