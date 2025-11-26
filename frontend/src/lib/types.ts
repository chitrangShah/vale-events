// Event data structure from the JSON API
export interface Event {
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

// A group of events with a label (e.g., "Today", "This Week")
export interface EventGroup {
  label: string;
  events: Event[];
}

// Group labels in display order
export const GROUP_LABELS = [
  'Today',
  'Tomorrow',
  'This Week',
  'Next Week',
  'Later'
] as const;

export type GroupLabel = (typeof GROUP_LABELS)[number];