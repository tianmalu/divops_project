import { createTheme, MantineProvider } from "@mantine/core";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import App from "./App.tsx";
import "@mantine/core/styles.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const theme = createTheme({});
const queryClient = new QueryClient();

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
					<App />
				</MantineProvider>
			</BrowserRouter>
		</QueryClientProvider>
	</StrictMode>,
);
