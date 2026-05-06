import { ref, computed } from 'vue'
import { useApi, type Image, type SessionPreset } from './useApi'
import { useTimer } from './useTimer'

export function useSession() {
  const api = useApi()
  const timer = useTimer()

  const images = ref<Image[]>([])
  const currentIndex = ref(0)
  const durationSeconds = ref(0)
  const isSessionActive = ref(false)
  const isSessionComplete = ref(false)

  // Current image being displayed
  const currentImage = computed(() => {
    return images.value[currentIndex.value] ?? null
  })

  // URL for current image
  const currentImageUrl = computed(() => {
    if (!currentImage.value) return ''
    return api.getImageUrl(currentImage.value.id)
  })

  // Progress through session (e.g., "3 / 10")
  const sessionProgress = computed(() => {
    return `${currentIndex.value + 1} / ${images.value.length}`
  })

  // Start a new session with a preset
  async function startSession(preset: SessionPreset) {
    images.value = await api.getRandomImages(preset.image_count)
    durationSeconds.value = preset.duration_seconds
    currentIndex.value = 0
    isSessionActive.value = true
    isSessionComplete.value = false
    
    timer.start(durationSeconds.value)
  }

  // Move to next image
  function nextImage() {
    if (currentIndex.value < images.value.length - 1) {
      currentIndex.value++
      timer.start(durationSeconds.value)
    } else {
      // Session complete
      endSession()
    }
  }

  // Skip to next image early
  function skip() {
    nextImage()
  }

  // Pause the timer
  function pause() {
    timer.pause()
  }

  // Resume the timer
  function resume() {
    timer.resume()
  }

  // End the session
  function endSession() {
    timer.cleanup()
    isSessionActive.value = false
    isSessionComplete.value = true
  }

  // Reset everything
  function reset() {
    timer.cleanup()
    images.value = []
    currentIndex.value = 0
    isSessionActive.value = false
    isSessionComplete.value = false
  }

  return {
    // State
    images,
    currentIndex,
    currentImage,
    currentImageUrl,
    sessionProgress,
    isSessionActive,
    isSessionComplete,
    
    // Timer passthrough
    displayTime: timer.displayTime,
    progress: timer.progress,
    isRunning: timer.isRunning,
    
    // Actions
    startSession,
    nextImage,
    skip,
    pause,
    resume,
    endSession,
    reset
  }
}