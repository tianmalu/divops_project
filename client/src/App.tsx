import { Container, useMantineColorScheme } from "@mantine/core";
import { Route, Routes } from "react-router";
import Login from "./pages/Authentication/Login/Login";
import Signup from "./pages/Authentication/Signup/Signup";
import Discussions from "./pages/User/Discussions/Discussions";
import Feed from "./pages/User/Feed/Feed";
import UserDashboard from "./pages/User/UserDashboard/UserDashboard";

const App = () => {
	const { setColorScheme } = useMantineColorScheme();
	setColorScheme("dark");
	return (
		<Container fluid w={"100%"} h={"100%"} p={0} m={0}>
			<Routes>
				<Route path="/" element={<h1>Main Page: Deployment Working</h1>} />
				<Route path="/login" element={<Login />} />
				<Route path="/signup" element={<Signup />} />
				<Route path="/main" element={<UserDashboard />}>
					<Route path="discussions" element={<Discussions />} />
					<Route path="feed" element={<Feed />} />
				</Route>
				<Route path="/*" element={<h1>404 Page Not Found</h1>} />
			</Routes>
		</Container>
	);
};

export default App;
