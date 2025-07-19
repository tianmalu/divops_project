import createClient, { type Middleware } from "openapi-fetch";
import type { paths as usersServicePaths } from "../../users_service_types";

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

// TODO change to actual route based on url
export const usersClient = createClient<usersServicePaths>({
	baseUrl: "http://localhost:8081/",
});

usersClient.use(myMiddleware);
export type usersSchema = usersServicePaths;
