/**
 * Event utility functions for filtering and grouping events.
 */

import type { Event, EventGroup, GroupLabel } from './types';
import { GROUP_LABELS } from './types';
import { parseEventDate, getDaysDifference, getDaysUntilSaturday } from './dateUtils';

/**
 * Determine which group label an event belongs to based on its date.
 *
 * @param eventDate - Parsed event date (or null for TBA)
 * @param today - Today's date at midnight
 * @returns The group label for this event
 */
export function getGroupLabel(eventDate: Date | null, today: Date): GroupLabel {
  // Events without dates go to "Later". This should not happen but is a safeguard.
  if (!eventDate) {
    return 'Later';
  }

  const daysDiff = getDaysDifference(eventDate, today);

  // Today
  if (daysDiff === 0) {
    return 'Today';
  }

  // Tomorrow
  if (daysDiff === 1) {
    return 'Tomorrow';
  }

  // This Week: remaining days until Saturday
  const daysUntilSaturday = getDaysUntilSaturday(today);
  if (daysDiff <= daysUntilSaturday) {
    return 'This Week';
  }

  // Next Week: following Sunday through Saturday
  const daysUntilNextSaturday = daysUntilSaturday + 7;
  if (daysDiff <= daysUntilNextSaturday) {
    return 'Next Week';
  }

  // Everything else
  return 'Later';
}

/**
 * Check if an event is in the past (before today).
 *
 * @param event - The event to check
 * @param today - Today's date at midnight
 * @returns true if event is in the past, false otherwise
 */
export function isEventPast(event: Event, today: Date): boolean {
  const eventDate = parseEventDate(event.date);

  // Events with no date are not considered past
  if (!eventDate) 
    return false;

  return eventDate < today;
}

/**
 * Sort events by date (earliest first, null dates at end).
 *
 * @param events - Array of events to sort
 * @returns New sorted array (does not mutate original)
 */
export function sortEventsByDate(events: Event[]): Event[] {
  return [...events].sort((a, b) => {
    const dateA = parseEventDate(a.date);
    const dateB = parseEventDate(b.date);

    // Null dates go to the end
    if (!dateA && !dateB) 
        return 0;

    if (!dateA) 
        return 1;
    
    if (!dateB) 
        return -1;

    return dateA.getTime() - dateB.getTime();
  });
}

/**
 * Filter out past events and group the remaining events by time period.
 * This is the main function that orchestrates the filtering and grouping.
 *
 * @param events - Raw events from API
 * @param today - Today's date (passed in for testability)
 * @returns Array of event groups in chronological order
 */
export function filterAndGroupEvents(events: Event[], today: Date): EventGroup[] {
  // Step 1: Filter out past events
  const upcomingEvents = events.filter((event) => !isEventPast(event, today));

  // Step 2: Sort by date
  const sortedEvents = sortEventsByDate(upcomingEvents);

  // Step 3: Group events by label
  const groupMap = new Map<GroupLabel, Event[]>();

  // Initialize empty arrays for each group
  for (const label of GROUP_LABELS) {
    groupMap.set(label, []);
  }

  // Assign each event to its group
  for (const event of sortedEvents) {
    const eventDate = parseEventDate(event.date);
    const label = getGroupLabel(eventDate, today);
    groupMap.get(label)!.push(event);
  }

  // Step 4: Convert to array, excluding empty groups
  const result: EventGroup[] = [];

  for (const label of GROUP_LABELS) {
    const groupEvents = groupMap.get(label)!;
    if (groupEvents.length > 0) {
      result.push({ label, events: groupEvents });
    }
  }

  return result;
}