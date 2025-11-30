import { parseTimeRange } from '../timeUtils';

describe('parseTimeRange', () => {
  test('returns null for empty', () => {
    expect(parseTimeRange(null)).toBeNull();
    expect(parseTimeRange('')).toBeNull();
  });

  test('parses complete time range', () => {
    expect(parseTimeRange('10 AM-2 PM')).toEqual({ startTime: '10 AM', endTime: '2 PM' });
  });

  test('extracts first time from complex schedule', () => {
    expect(parseTimeRange('Tuesdays-Fridays 10:00-4:00, Weekends 12:00-4:00')).toEqual({
      startTime: '10:00 AM',
      endTime: '4:00 PM'
    });
  });

  test('handles to separator', () => {
    expect(parseTimeRange('10 to 5')).toEqual({ startTime: '10 AM', endTime: '5 PM' });
  });

  test('inherits PM when start <= end', () => {
    expect(parseTimeRange('4-4:45 PM')).toEqual({ startTime: '4 PM', endTime: '4:45 PM' });
  });

  test('uses AM when start > end and end is PM', () => {
    expect(parseTimeRange('10-2 PM')).toEqual({ startTime: '10 AM', endTime: '2 PM' });
  });

  test('single time uses same for start and end', () => {
    expect(parseTimeRange('6:00 PM')).toEqual({ startTime: '6:00 PM', endTime: '6:00 PM' });
    expect(parseTimeRange('8:00 PM')).toEqual({ startTime: '8:00 PM', endTime: '8:00 PM' });
  });

  test('handles p.m. and a.m. with dots', () => {
    expect(parseTimeRange('1 p.m. - 4 p.m.')).toEqual({ startTime: '1 p.m.', endTime: '4 p.m.' });
    expect(parseTimeRange('10 a.m. - 2 p.m.')).toEqual({ startTime: '10 a.m.', endTime: '2 p.m.' });
  });
});