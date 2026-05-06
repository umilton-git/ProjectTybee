import { ref, computed } from 'vue'

export function useTimer() {
  const totalSeconds = ref(0)
  const remainingSeconds = ref(0)
  const isRunning = ref(false)
  
  let intervalId: number | null = null

  // Computed property: format as "MM:SS"
  const displayTime = computed(() => {
    const mins = Math.floor(remainingSeconds.value / 60)
    const secs = remainingSeconds.value % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  })

  // Computed property: progress percentage (for progress bar)
  const progress = computed(() => {
    if (totalSeconds.value === 0) return 0
    return ((totalSeconds.value - remainingSeconds.value) / totalSeconds.value) * 100
  })

  // Start the timer
  function start(seconds: number) {
    totalSeconds.value = seconds
    remainingSeconds.value = seconds
    resume()
  }

  // Pause the timer
  function pause() {
    isRunning.value = false
    if (intervalId !== null) {
      clearInterval(intervalId)
      intervalId = null
    }
  }

  // Resume the timer
  function resume() {
    if (isRunning.value) return
    isRunning.value = true
    
    intervalId = window.setInterval(() => {
      if (remainingSeconds.value > 0) {
        remainingSeconds.value--
      } else {
        pause()
      }
    }, 1000)
  }

  // Reset the timer (optionally with a new duration)
  function reset(seconds?: number) {
    pause()
    remainingSeconds.value = seconds ?? totalSeconds.value
  }

  // Cleanup on finish
  function cleanup() {
    pause()
  }

  return {
    remainingSeconds,
    isRunning,
    displayTime,
    progress,
    start,
    pause,
    resume,
    reset,
    cleanup
  }
}