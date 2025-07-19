import createClient, { type Middleware } from "openapi-fetch";
import type { paths as usersServicePaths } from "../../users_service_types";

const myMiddleware: Middleware = {
	//   async onRequest({ request, options }) {
	//     // set "foo" header
	//     request.headers.set("foo", "bar");
	//     return request;
	//   },
	async onResponse({ response }) {
		if (!response.ok) {
			const text = await response.text();
			throw new Error(text);
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
