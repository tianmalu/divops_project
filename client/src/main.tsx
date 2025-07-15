import { createTheme, MantineProvider } from "@mantine/core";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import App from "./App.tsx";

const theme = createTheme({});

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<BrowserRouter>
			<MantineProvider
				forceColorScheme="dark"
				defaultColorScheme="dark"
				theme={theme}
			>
				<App />
			</MantineProvider>
		</BrowserRouter>
	</StrictMode>,
);
