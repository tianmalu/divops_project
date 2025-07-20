import { createTheme, MantineProvider } from "@mantine/core";
import { fireEvent, render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Login from "./Login";
import "@testing-library/jest-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// Helper to render with router context
const renderWithRouter = (ui: React.ReactElement) => {
	const theme = createTheme({});
	const queryClient = new QueryClient({
		defaultOptions: {
			queries: {
				refetchOnWindowFocus: false,
			},
		},
	});

	return render(
		<BrowserRouter>
			<QueryClientProvider client={queryClient}>
				<MantineProvider
					forceColorScheme="dark"
					defaultColorScheme="dark"
					theme={theme}
				>
					{ui}
				</MantineProvider>
			</QueryClientProvider>
		</BrowserRouter>,
	);
};

describe("Login Component", () => {
	it("renders the title and signup link", () => {
		renderWithRouter(<Login />);

		expect(screen.getByText(/welcome back! helm/i)).toBeInTheDocument();
		expect(screen.getByText(/create account/i)).toBeInTheDocument();
	});

	it("renders the email and password fields", () => {
		renderWithRouter(<Login />);

		expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
		expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
	});

	it("shows validation errors when submitting empty form", () => {
		renderWithRouter(<Login />);

		fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

		expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
		expect(screen.getByText(/password required/i)).toBeInTheDocument();
	});

	// it("navigates on successful submit (mock)", () => {
	// 	// Mock navigate
	// 	const mockedNavigate = jest.fn();
	// 	jest.mock("react-router", () => ({
	// 		...jest.requireActual("react-router"),
	// 		useNavigate: () => mockedNavigate
	// 	}));

	// 	renderWithRouter(<Login />);

	// 	fireEvent.change(screen.getByLabelText(/email/i), {
	// 		target: { value: "test@example.com" },
	// 	});
	// 	fireEvent.change(screen.getByLabelText(/password/i), {
	// 		target: { value: "password123" },
	// 	});
	// 	fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

	// 	// This won't work directly unless you re-inject the mocked navigate
	// 	// For a real test, you'd inject `navigate` as a prop or refactor
	// });
});
