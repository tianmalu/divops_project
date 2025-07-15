import { AppShell, Container } from "@mantine/core";
import { Outlet } from "react-router";
import UserNavbar from "./UserNavbar/UserNavbar";

const UserDashboard = () => {
	return (
		<AppShell navbar={{ width: 200, breakpoint: "sm" }} padding="md">
			<AppShell.Navbar>
				<UserNavbar />
			</AppShell.Navbar>
			<AppShell.Main display="flex" flex={1}>
				<Container fluid w={"100%"}>
					<Outlet />
				</Container>
			</AppShell.Main>
		</AppShell>
	);
};

export default UserDashboard;
