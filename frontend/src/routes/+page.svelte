<script lang="ts">
  import { onMount } from 'svelte';
  import { injectAnalytics } from '@vercel/analytics/sveltekit'

  interface Event {
    id: string;
    name: string;
    date: string | null;
    time: string | null;
    location: string | null;
    address: string | null;
    description: string | null;
    organization: string | null;
    price: string | null;
    image_path: string;
  }

  let events: Event[] = [];
  let loading = true;
  let error = '';
  let selectedImage: string | null = null;

  onMount(async () => {
    try {
      // Fetch from static JSON file (no backend needed!)
      const response = await fetch('/api/events.json');
      const data = await response.json();
      events = data.events;
    } catch (err) {
      error = 'Failed to load events';
      console.error(err);
    } finally {
      loading = false;
    }
  });

  // Get image from static folder
  function getImageUrl(imagePath: string): string {
    const filename = imagePath.split('/').pop();
    return `/images/${filename}`;
  }

  function viewImage(imagePath: string) {
    selectedImage = getImageUrl(imagePath);
  }

  function closeModal() {
    selectedImage = null;
  }

  // Calendar functionality
  function formatDate(dateStr: string | null): string {
    if (!dateStr) return 'Date TBA';
    
    // Parse as local date to avoid timezone issues
    const [year, month, day] = dateStr.split('-').map(Number);
    const date = new Date(year, month - 1, day); // month is 0-indexed
    
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }

  function addToCalendar(event: Event) {
    if (!event.date) {
      alert('Event date not available');
      return;
    }

    // Parse date locally to avoid timezone issues
    const [year, month, day] = event.date.split('-').map(Number);
    const eventDate = new Date(year, month - 1, day); // month is 0-indexed
    
    const startTime = event.time?.split('-')[0]?.trim() || '09:00';
    const endTime = event.time?.split('-')[1]?.trim() || '17:00';
    
    // Generate unique ID
    const uid = `${event.id}@vale-events.com`;
    
    // Current timestamp for DTSTAMP
    const now = new Date();
    const dtstamp = formatICSDate(now, '00:00');
    
    // Format start and end times
    const dtstart = formatICSDate(eventDate, startTime);
    const dtend = formatICSDate(eventDate, endTime);
    
    // Create ICS content with proper line endings
    const ics = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//Vale Events//Event Calendar//EN',
      'BEGIN:VEVENT',
      `UID:${uid}`,
      `DTSTAMP:${dtstamp}`,
      `DTSTART:${dtstart}`,
      `DTEND:${dtend}`,
      `SUMMARY:${event.name}`,
      `DESCRIPTION:${event.description || ''}`,
      `LOCATION:${event.address || event.location || ''}`,
      'STATUS:CONFIRMED',
      'SEQUENCE:0',
      'END:VEVENT',
      'END:VCALENDAR'
    ].join('\r\n');

    // Download .ics file
    const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${event.name.replace(/[^a-z0-9]/gi, '_')}.ics`;
    link.click();
    URL.revokeObjectURL(url);
  }

  function formatICSDate(date: Date, time: string): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    
    // Parse time (e.g., "10:00 AM" or "1:00 PM")
    const timeMatch = time.match(/(\d+):?(\d+)?\s*(am|pm)?/i);
    let hours = timeMatch ? parseInt(timeMatch[1]) : 9;
    const minutes = timeMatch?.[2] || '00';
    const ampm = timeMatch?.[3]?.toLowerCase();
    
    if (ampm === 'pm' && hours < 12) hours += 12;
    if (ampm === 'am' && hours === 12) hours = 0;
    
    const hoursStr = String(hours).padStart(2, '0');
    
    return `${year}${month}${day}T${hoursStr}${minutes}00`;
  }
</script>

<svelte:head>
  <title>Vale Events</title>
</svelte:head>

<div class="container">
  <header>
    <h1>Vale Events</h1>
    <p class="subtitle">Discover upcoming events in your area</p>
  </header>

  {#if loading}
    <div class="loading">
      <div class="spinner"></div>
      <p>Loading events...</p>
    </div>
  {:else if error}
    <div class="error-box">
      <p>{error}</p>
    </div>
  {:else if events.length === 0}
    <div class="empty-state">
      <p>No events found. Check back soon!</p>
    </div>
  {:else}
    <div class="events-grid">
      {#each events as event}
        <article class="event-card">
          <div class="event-image" on:click={() => viewImage(event.image_path)} on:keydown={(e) => e.key === 'Enter' && viewImage(event.image_path)} role="button" tabindex="0">
            <img src={getImageUrl(event.image_path)} alt={event.name} />
            {#if event.price}
              <span class="price-badge">{event.price}</span>
            {/if}
            <div class="image-overlay">
              <svg class="zoom-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
                <line x1="11" y1="8" x2="11" y2="14"></line>
                <line x1="8" y1="11" x2="14" y2="11"></line>
              </svg>
              <span>Click to view</span>
            </div>
          </div>
          
          <div class="event-content">
            <h2 class="event-name">{event.name}</h2>
            
            {#if event.organization}
              <p class="organization">{event.organization}</p>
            {/if}

            <div class="event-details">
              {#if event.date}
                <div class="detail">
                  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  <span>{formatDate(event.date)}</span>
                </div>
              {/if}

              {#if event.time}
                <div class="detail">
                  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  <span>{event.time}</span>
                </div>
              {/if}

              {#if event.address || event.location}
                <div class="detail">
                  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                  <span>{event.address || event.location}</span>
                </div>
              {/if}
            </div>

            {#if event.description}
              <p class="description">{event.description}</p>
            {/if}

            <button class="calendar-btn" on:click={() => addToCalendar(event)}>
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              Add to Calendar
            </button>
          </div>
        </article>
      {/each}
    </div>
  {/if}

  {#if selectedImage}
    <div class="modal" on:click={closeModal} on:keydown={(e) => e.key === 'Escape' && closeModal()} role="button" tabindex="0">
      <div class="modal-content" on:click={(e) => e.stopPropagation()} on:keydown={() => {}} role="button" tabindex="0">
        <button class="close-btn" on:click={closeModal}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <img src={selectedImage} alt="Event flyer" />
      </div>
    </div>
  {/if}
</div>

<style>
  /* Use the same beautiful styles from before */
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  header {
    text-align: center;
    margin-bottom: 3rem;
    color: white;
  }

  h1 {
    font-size: 3rem;
    margin: 0 0 0.5rem 0;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
  }

  .subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    margin: 0;
  }

  .loading {
    text-align: center;
    padding: 4rem 0;
    color: white;
  }

  .spinner {
    width: 50px;
    height: 50px;
    margin: 0 auto 1rem;
    border: 4px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .error-box {
    background: #fee;
    color: #c33;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
  }

  .empty-state {
    background: rgba(255,255,255,0.9);
    padding: 3rem;
    border-radius: 12px;
    text-align: center;
    color: #666;
  }

  .events-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
  }

  .event-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .event-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.25);
  }

  .event-image {
    position: relative;
    width: 100%;
    height: 250px;
    overflow: hidden;
    background: #f0f0f0;
  }

  .event-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .price-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: #10b981;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }

  .event-content {
    padding: 1.5rem;
  }

  .event-name {
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    color: #1f2937;
    line-height: 1.3;
  }

  .organization {
    margin: 0 0 1rem 0;
    color: #6b7280;
    font-size: 0.95rem;
    font-weight: 500;
  }

  .event-details {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  .detail {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #4b5563;
    font-size: 0.95rem;
  }

  .icon {
    width: 18px;
    height: 18px;
    stroke-width: 2;
    flex-shrink: 0;
  }

  .description {
    margin: 1rem 0;
    color: #6b7280;
    font-size: 0.95rem;
    line-height: 1.5;
  }

  .calendar-btn {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-top: 1rem;
  }

  .calendar-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  .calendar-btn:active {
    transform: translateY(0);
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 2rem;
    }

    .subtitle {
      font-size: 1rem;
    }

    .events-grid {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    .event-image {
      height: 200px;
    }

    .container {
      padding: 1.5rem 1rem;
    }
  }

  @media (max-width: 480px) {
    h1 {
      font-size: 1.75rem;
    }

    .event-name {
      font-size: 1.25rem;
    }

    .event-content {
      padding: 1rem;
    }
  }

  .event-image {
    position: relative;
    width: 100%;
    height: 250px;
    overflow: hidden;
    background: #f0f0f0;
    cursor: pointer;
  }

  .image-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    opacity: 0;
    transition: all 0.3s ease;
    color: white;
    font-weight: 600;
  }

  .event-image:hover .image-overlay {
    background: rgba(0, 0, 0, 0.6);
    opacity: 1;
  }

  .zoom-icon {
    width: 48px;
    height: 48px;
    stroke-width: 2;
  }

  .modal {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 2rem;
  }

  .modal-content {
    position: relative;
    max-width: 90vw;
    max-height: 90vh;
  }

  .modal-content img {
    max-width: 100%;
    max-height: 90vh;
    object-fit: contain;
    border-radius: 8px;
  }

  .close-btn {
    position: absolute;
    top: -3rem;
    right: 0;
    background: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease;
  }

  .close-btn:hover {
    transform: scale(1.1);
  }

  .close-btn svg {
    width: 24px;
    height: 24px;
    stroke-width: 2;
    stroke: #333;
  }
</style>