import { render, screen } from "@testing-library/react";
import { MemoryRouter, useNavigate } from "react-router-dom";
import '@testing-library/jest-dom';

function TestComponent() {
  const navigate = useNavigate();
  return <button onClick={() => navigate("/")}>Go Home</button>;
}


test("navigate works", () => {
  render(
    <MemoryRouter>
      <TestComponent />
    </MemoryRouter>
  );
  expect(screen.getByRole("button")).toBeInTheDocument();
});




// import { createTheme, MantineProvider } from "@mantine/core";
// import { fireEvent, render, screen } from "@testing-library/react";
// import { MemoryRouter, useNavigate } from "react-router-dom";
// import Login from "./Login";
// import "@testing-library/jest-dom";
// import { QueryClient, QueryClientProvider } from "@tanstack/react-query";


// // Helper to render with router context
// const renderWithRouter = (ui: React.ReactElement) => {
// 	const theme = createTheme({});
// 	const queryClient = new QueryClient({
// 		defaultOptions: {
// 			queries: {
// 				refetchOnWindowFocus: false,
// 			},
// 		},
// 	});

// 	return render(
// 		<MemoryRouter>
// 			<QueryClientProvider client={queryClient}>
// 				<MantineProvider
// 					forceColorScheme="dark"
// 					defaultColorScheme="dark"
// 					theme={theme}
// 				>
// 					{ui}
// 				</MantineProvider>
// 			</QueryClientProvider>
// 		</MemoryRouter>,
// 	);
// };

// describe("Login Component", () => {
// 	it("renders the title and signup link", () => {
// 		renderWithRouter(<Login />);

// 		expect(screen.getByText(/welcome back! helm/i)).toBeInTheDocument();
// 		expect(screen.getByText(/create account/i)).toBeInTheDocument();
// 	});

// 	it("renders the email and password fields", () => {
// 		renderWithRouter(<Login />);

// 		expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
// 		expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
// 	});

// 	it("shows validation errors when submitting empty form", () => {
// 		renderWithRouter(<Login />);

// 		fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

// 		expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
// 		expect(screen.getByText(/password required/i)).toBeInTheDocument();
// 	});
// });
