// Interface for Image
export interface Image {
  id: number
  filename: string
  source: string
  uploaded_at: string
}

// Interface for Session Preset
export interface SessionPreset {
  id: number
  name: string
  image_count: number
  duration_seconds: number
}

// API URL
const API_BASE = 'http://localhost:8000'

export function useApi() {
  
  // Fetch all session presets
  async function getPresets(): Promise<SessionPreset[]> {
    const response = await fetch(`${API_BASE}/presets`)
    if (!response.ok) throw new Error('Failed to fetch presets')
    return response.json()
  }

  // Fetch random images for a session
  async function getRandomImages(count: number): Promise<Image[]> {
    const response = await fetch(`${API_BASE}/images/random?count=${count}`)
    if (!response.ok) throw new Error('Failed to fetch images')
    return response.json()
  }

  // Get the URL for an image file
  function getImageUrl(imageId: number): string {
    return `${API_BASE}/images/${imageId}/file`
  }

  // Upload a new image
  async function uploadImage(file: File): Promise<Image> {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch(`${API_BASE}/images/upload`, {
      method: 'POST',
      body: formData
    })
    if (!response.ok) throw new Error('Failed to upload image')
    return response.json()
  }

  return {
    getPresets,
    getRandomImages,
    getImageUrl,
    uploadImage
  }
}