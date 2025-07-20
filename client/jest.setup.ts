import '@testing-library/jest-dom';
// import { TextEncoder, TextDecoder } from 'fast-text-encoding';

// (global as any).TextEncoder = global.TextEncoder;
// (global as any).TextDecoder = global.TextDecoder;

Object.defineProperty(import.meta, 'env', {
  value: {
    VITE_USERS_SERVICE_API_BASE_URL: 'http://mocked-url.com',
        VITE_DISCUSSIONS_SERVICE_API_BASE_URL: 'http://mocked-url.com'
  }
});