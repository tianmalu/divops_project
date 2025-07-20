import '@testing-library/jest-dom';
import { vi } from 'vitest';


Object.defineProperty(import.meta, 'env', {
  value: {
    VITE_USERS_SERVICE_API_BASE_URL: 'http://mocked-url.com/'
  }
});


window.matchMedia = vi.fn().mockImplementation(query => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: vi.fn(),
  removeListener: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  dispatchEvent: vi.fn(),
}));
