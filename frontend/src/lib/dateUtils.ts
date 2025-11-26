/**
 * Date utility functions for event processing
 */

/**
 * Get today's date at midnight (start of day).
 */
export function getToday(): Date {
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate());
}

/**
 * Parse an event date string (YYYY-MM-DD) into a Date object.
 * Returns null if the date string is invalid or null.
 *
 * @param dateStr - Date string in "YYYY-MM-DD" format
 * @returns Date object at midnight, or null if invalid
 */
export function parseEventDate(dateStr: string | null): Date | null {
  if (!dateStr) 
    return null;

  const parts = dateStr.split('-');
  if (parts.length !== 3) 
    return null;

  const [year, month, day] = parts.map(Number);

  // Check for valid numbers
  if (isNaN(year) || isNaN(month) || isNaN(day)) 
    return null;

  if (year < 1 || month < 1 || month > 12 || day < 1 || day > 31) 
    return null;

  return new Date(year, month - 1, day); // month is 0-indexed in JS
}

/**
 * Calculate the difference in days between two dates.
 * Positive result means date1 is after date2.
 *
 * @param date1 - First date
 * @param date2 - Second date
 * @returns Number of days difference (can be negative)
 */
export function getDaysDifference(date1: Date, date2: Date): number {
  const msPerDay = 24 * 60 * 60 * 1000;
  return Math.floor((date1.getTime() - date2.getTime()) / msPerDay);
}

/**
 * Calculate days remaining until Saturday (end of week).
 * Week starts on Sunday (day 0), ends on Saturday (day 6).
 *
 * @param date - The reference date
 * @returns Number of days until Saturday (0-6)
 */
export function getDaysUntilSaturday(date: Date): number {
  const dayOfWeek = date.getDay(); // 0 = Sunday, 6 = Saturday
  return 6 - dayOfWeek;
}