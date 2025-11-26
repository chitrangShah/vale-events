import type { Event } from '../types';
import { getGroupLabel, isEventPast, sortEventsByDate, filterAndGroupEvents } from '../eventUtils';

// Helper to create a mock event
function createEvent(id: string, date: string | null): Event {
  return {
    id,
    name: `Event ${id}`,
    date,
    time: null,
    location: null,
    address: null,
    description: null,
    organization: null,
    price: null,
    image_path: ''
  };
}

// Month is 0 indexed so December is 11
describe('getGroupLabel', () => {
  // Use a fixed "today" for consistent tests
  const today = new Date(2025, 10, 25);

  test('returns "Today" for same day', () => {
    const eventDate = new Date(2025, 10, 25);
    expect(getGroupLabel(eventDate, today)).toBe('Today');
  });

  test('returns "Tomorrow" for next day', () => {
    const eventDate = new Date(2025, 10, 26);
    expect(getGroupLabel(eventDate, today)).toBe('Tomorrow');
  });

  test('returns "This Week" for days until Saturday', () => {
    const eventDate = new Date(2025, 10, 28);
    expect(getGroupLabel(eventDate, today)).toBe('This Week');
  });

  test('returns "Next Week" for following week', () => {
    const nextSunday = new Date(2025, 10, 30);
    expect(getGroupLabel(nextSunday, today)).toBe('Next Week');

    const nextSaturday = new Date(2025, 11, 6);
    expect(getGroupLabel(nextSaturday, today)).toBe('Next Week');
  });

  test('returns "Later" for dates beyond next week', () => {
    const farFuture = new Date(2025, 11, 20);
    expect(getGroupLabel(farFuture, today)).toBe('Later');
  });

  test('returns "Later" for null date', () => {
    expect(getGroupLabel(null, today)).toBe('Later');
  });
});

describe('isEventPast', () => {
    // October 25, 2025 (month is 0-indexed: 9 = October)
  const today = new Date(2025, 9, 25);

  test('returns true for past events', () => {
    const pastEvent = createEvent('1', '2025-10-18');
    expect(isEventPast(pastEvent, today)).toBe(true);
  });

  test('returns false for today events', () => {
    const todayEvent = createEvent('1', '2025-10-25');
    expect(isEventPast(todayEvent, today)).toBe(false);
  });

  test('returns false for future events', () => {
    const futureEvent = createEvent('1', '2025-10-27');
    expect(isEventPast(futureEvent, today)).toBe(false);
  });

  test('returns false for events with no date', () => {
    const noDateEvent = createEvent('1', null);
    expect(isEventPast(noDateEvent, today)).toBe(false);
  });
});

describe('sortEventsByDate', () => {
  test('sorts events chronologically', () => {
    const events = [
      createEvent('3', '2025-10-25'),
      createEvent('1', '2025-10-20'),
      createEvent('2', '2025-10-22')
    ];

    const sorted = sortEventsByDate(events);

    expect(sorted[0].id).toBe('1');
    expect(sorted[1].id).toBe('2');
    expect(sorted[2].id).toBe('3'); 
  });

  test('places null dates at the end', () => {
    const events = [
      createEvent('2', null),
      createEvent('1', '2025-10-20'),
      createEvent('3', null)
    ];

    const sorted = sortEventsByDate(events);

    expect(sorted[0].id).toBe('1'); // Has date, comes first
    expect(sorted[1].date).toBeNull();
    expect(sorted[2].date).toBeNull();
  });

  test('does not mutate original array', () => {
    const events = [createEvent('2', '2025-10-25'), createEvent('1', '2025-10-20')];

    sortEventsByDate(events);

    expect(events[0].id).toBe('2'); // Original unchanged
  });
});

describe('filterAndGroupEvents', () => {
  // Sunday, October 19, 2025 (month 9 = October)
  // Week: Sun Oct 19 - Sat Oct 25
  const today = new Date(2025, 9, 19);

  test('filters out past events', () => {
    const events = [
      createEvent('past', '2025-10-18'),
      createEvent('today', '2025-10-19'),
      createEvent('future', '2025-10-20')
    ];

    const groups = filterAndGroupEvents(events, today);
    const allEventIds = groups.flatMap((g) => g.events.map((e) => e.id));

    expect(allEventIds).not.toContain('past');
    expect(allEventIds).toContain('today');
    expect(allEventIds).toContain('future');
  });

  test('groups events correctly', () => {
    const events = [
      createEvent('today', '2025-10-19'),      // Sunday - Today
      createEvent('tomorrow', '2025-10-20'),   // Monday - Tomorrow
      createEvent('thisWeek', '2025-10-23'),   // Thursday - This Week
      createEvent('nextWeek', '2025-10-27'),   // Next Monday - Next Week
      createEvent('later', '2025-11-15'),      // November - Later
    ];

    const groups = filterAndGroupEvents(events, today);

    const findGroup = (label: string) => groups.find((g) => g.label === label);

    expect(findGroup('Today')?.events[0].id).toBe('today');
    expect(findGroup('Tomorrow')?.events[0].id).toBe('tomorrow');
    expect(findGroup('This Week')?.events[0].id).toBe('thisWeek');
    expect(findGroup('Next Week')?.events[0].id).toBe('nextWeek');
    expect(findGroup('Later')?.events[0].id).toBe('later');
  });

  test('excludes empty groups', () => {
    const events = [createEvent('today', '2025-10-19')];

    const groups = filterAndGroupEvents(events, today);

    expect(groups).toHaveLength(1);
    expect(groups[0].label).toBe('Today');
  });

  test('returns empty array when all events are past', () => {
    const events = [
      createEvent('past1', '2025-10-17'),
      createEvent('past2', '2025-10-18')
    ];

    const groups = filterAndGroupEvents(events, today);

    expect(groups).toHaveLength(0);
  });
});