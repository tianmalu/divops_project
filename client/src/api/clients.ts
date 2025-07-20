import createClient, { type Middleware } from "openapi-fetch";
import type { paths as usersServicePaths } from "../../users_service_types";

const VITE_USERS_SERVICE_API_BASE_URL =  import.meta.env.VITE_USERS_SERVICE_API_BASE_URL

const myMiddleware: Middleware = {
	async onRequest({ request }) {
		const token = localStorage.getItem("token");
		if (token) {
			request.headers.set("Authorization", `Bearer ${token}`);
			return request;
		}
		return undefined;
	},
	async onResponse({ response }) {
		if (!response.ok) {
			let message = `Request failed with status ${response.status}`;

			try {
				const text = await response.text();
				if (text) {
					const errorData = JSON.parse(text);
					if (errorData.message) {
						message = errorData.message;
					}
				}
			} catch {
				// Ignore parsing errors
			}

			throw new Error(message);
		}
		return undefined;
	},
};

export const usersClient = createClient<usersServicePaths>({
	baseUrl: VITE_USERS_SERVICE_API_BASE_URL || "",
});

usersClient.use(myMiddleware);
export type usersSchema = usersServicePaths;
