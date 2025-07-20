import { createTheme, MantineProvider } from "@mantine/core";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import App from "./App.tsx";
import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";
import { Notifications } from "@mantine/notifications";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const theme = createTheme({});
const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			refetchOnWindowFocus: false,
		},
	},
});

// biome-ignore lint/style/noNonNullAssertion: no reason
createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<QueryClientProvider client={queryClient}>
			<BrowserRouter>
				<MantineProvider
					forceColorScheme="dark"
					defaultColorScheme="dark"
					theme={theme}
				>
					<Notifications />
					<App />
				</MantineProvider>
			</BrowserRouter>
		</QueryClientProvider>
	</StrictMode>,
);
