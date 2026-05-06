import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { useSession } from '../useSession'

// Mock the API module
vi.mock('../useApi', () => ({
  useApi: () => ({
    getPresets: vi.fn(),
    getRandomImages: vi.fn().mockResolvedValue([
      { id: 1, filename: 'test1.jpg', source: 'local', uploaded_at: '2026-05-06' },
      { id: 2, filename: 'test2.jpg', source: 'local', uploaded_at: '2026-05-06' },
      { id: 3, filename: 'test3.jpg', source: 'local', uploaded_at: '2026-05-06' },
    ]),
    getImageUrl: (id: number) => `http://localhost:8000/images/${id}/file`
  })
}))

describe('useSession', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('starts inactive with no images', () => {
    const session = useSession()
    
    expect(session.isSessionActive.value).toBe(false)
    expect(session.images.value).toEqual([])
    expect(session.currentIndex.value).toBe(0)
  })

  it('starts a session with preset', async () => {
    const session = useSession()
    
    const preset = { id: 1, name: 'Test', image_count: 3, duration_seconds: 30 }
    await session.startSession(preset)
    
    expect(session.isSessionActive.value).toBe(true)
    expect(session.images.value.length).toBe(3)
    expect(session.currentIndex.value).toBe(0)
    expect(session.isRunning.value).toBe(true)
  })

  it('generates correct image URL', async () => {
    const session = useSession()
    
    const preset = { id: 1, name: 'Test', image_count: 3, duration_seconds: 30 }
    await session.startSession(preset)
    
    expect(session.currentImageUrl.value).toBe('http://localhost:8000/images/1/file')
  })

  it('advances to next image on skip', async () => {
    const session = useSession()
    
    const preset = { id: 1, name: 'Test', image_count: 3, duration_seconds: 30 }
    await session.startSession(preset)
    
    expect(session.currentIndex.value).toBe(0)
    session.skip()
    expect(session.currentIndex.value).toBe(1)
  })

  it('shows correct session progress', async () => {
    const session = useSession()
    
    const preset = { id: 1, name: 'Test', image_count: 3, duration_seconds: 30 }
    await session.startSession(preset)
    
    expect(session.sessionProgress.value).toBe('1 / 3')
    session.skip()
    expect(session.sessionProgress.value).toBe('2 / 3')
  })

  it('ends session after last image', async () => {
    const session = useSession()
    
    const preset = { id: 1, name: 'Test', image_count: 3, duration_seconds: 30 }
    await session.startSession(preset)
    
    session.skip() // 1 -> 2
    session.skip() // 2 -> 3
    session.skip() // 3 -> end
    
    expect(session.isSessionActive.value).toBe(false)
    expect(session.isSessionComplete.value).toBe(true)
  })

  it('resets session state', async () => {
    const session = useSession()
    
    const preset = { id: 1, name: 'Test', image_count: 3, duration_seconds: 30 }
    await session.startSession(preset)
    session.skip()
    session.reset()
    
    expect(session.isSessionActive.value).toBe(false)
    expect(session.images.value).toEqual([])
    expect(session.currentIndex.value).toBe(0)
  })
})