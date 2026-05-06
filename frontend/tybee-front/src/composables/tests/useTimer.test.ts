import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { useTimer } from '../useTimer'

describe('useTimer', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('starts with correct duration', () => {
    const timer = useTimer()
    timer.start(30)
    
    expect(timer.remainingSeconds.value).toBe(30)
    expect(timer.isRunning.value).toBe(true)
  })

  it('counts down each second', () => {
    const timer = useTimer()
    timer.start(30)
    
    vi.advanceTimersByTime(1000)
    expect(timer.remainingSeconds.value).toBe(29)
    
    vi.advanceTimersByTime(5000)
    expect(timer.remainingSeconds.value).toBe(24)
  })

  it('pauses and resumes', () => {
    const timer = useTimer()
    timer.start(30)
    
    vi.advanceTimersByTime(5000)
    timer.pause()
    expect(timer.remainingSeconds.value).toBe(25)
    expect(timer.isRunning.value).toBe(false)
    
    vi.advanceTimersByTime(5000) // Should not count while paused
    expect(timer.remainingSeconds.value).toBe(25)
    
    timer.resume()
    vi.advanceTimersByTime(5000)
    expect(timer.remainingSeconds.value).toBe(20)
  })

  it('formats display time correctly', () => {
    const timer = useTimer()
    timer.start(125) // 2:05
    
    expect(timer.displayTime.value).toBe('2:05')
  })

  it('stops at zero', () => {
    const timer = useTimer()
    timer.start(3)
    
    vi.advanceTimersByTime(5000) // More than 3 seconds
    
    expect(timer.remainingSeconds.value).toBe(0)
    expect(timer.isRunning.value).toBe(false)
  })
})