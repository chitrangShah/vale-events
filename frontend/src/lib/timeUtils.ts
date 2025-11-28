export function parseTimeRange(timeStr: string | null): { startTime: string; endTime: string } | null {
  if (!timeStr || !timeStr.trim()) {
    return null;
  }

  // Step 1: Take first part before comma
  let s = timeStr.split(',')[0].trim();

  // Step 2: Replace "to" with dash
  s = s.replace(/ to /gi, '-');

  // Step 3: Split by dash
  const parts = s.split('-');
  if (parts.length < 2) {
    return null;
  }

  // Step 4: Extract time from each part (time starts at first digit)
  const times: string[] = [];
  for (const part of parts) {
    const time = extractTime(part.trim());
    if (time) {
      times.push(time);
    }
  }

  if (times.length < 2) {
    return null;
  }

  // Step 5: Use last two times found
  const start = times[times.length - 2];
  const end = times[times.length - 1];

  // Step 6: Add AM/PM
  return addAmPm(start, end);
}

function extractTime(part: string): string | null {
  // Find first digit
  for (let i = 0; i < part.length; i++) {
    if (part[i] >= '0' && part[i] <= '9') {
      return part.substring(i).trim();
    }
  }
  return null;
}

function addAmPm(start: string, end: string): { startTime: string; endTime: string } {
  const startLower = start.toLowerCase();
  const endLower = end.toLowerCase();
  const startHasAmPm = startLower.includes('am') || startLower.includes('pm');
  const endHasAmPm = endLower.includes('am') || endLower.includes('pm');

  if (startHasAmPm && endHasAmPm) {
    return { startTime: start, endTime: end };
  }

  const startHour = parseInt(start);
  const endHour = parseInt(end);

  if (endHasAmPm) {
    const endIsPm = endLower.includes('pm');
    if (endIsPm && startHour > endHour) {
      return { startTime: `${start} AM`, endTime: end };
    }
    return { startTime: `${start} ${endIsPm ? 'PM' : 'AM'}`, endTime: end };
  }

  if (startHour > endHour) {
    return { startTime: `${start} AM`, endTime: `${end} PM` };
  }
  if (startHour >= 6 && endHour <= 12) {
    return { startTime: `${start} AM`, endTime: `${end} AM` };
  }
  return { startTime: `${start} PM`, endTime: `${end} PM` };
}