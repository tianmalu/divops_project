/// <reference types="vite/client" />

interface ImportMetaEnv {
	readonly VITE_USERS_SERVICE_API_BASE_URL: string;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}
