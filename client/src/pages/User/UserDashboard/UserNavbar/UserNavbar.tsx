import { Box, Button, Group, Loader } from "@mantine/core";
import { IconBellRinging, IconLogout } from "@tabler/icons-react";
import { useState } from "react";
import { useNavigate } from "react-router";
import { useGetUserProfile } from "../../../../api/users-api";
import classes from "./UserNavbar.module.css";

const data = [
	{ link: "discussions", label: "Discussions", icon: IconBellRinging },
	{ link: "feed", label: "Feed", icon: IconBellRinging },
];

const UserNavbar = () => {
	const navigate = useNavigate();
	const [active, setActive] = useState("Billing");
	const { data: profileData, isFetching } = useGetUserProfile();
	console.log(profileData);
	const links = data.map((item) => (
		<Button
			justify="flex-start"
			w="100%"
			variant={item.label === active ? "default" : "transparent"}
			leftSection={<item.icon className={classes.linkIcon} stroke={1.5} />}
			key={item.label}
			onClick={() => {
				setActive(item.label);
				navigate(item.link);
			}}
		>
			{item.label}
		</Button>
	));

	const handleLogout = () => {
		localStorage.removeItem("token");
		navigate("/");
	};

	return (
		<nav className={classes.navbar}>
			<div className={classes.navbarMain}>
				<Group className={classes.header} justify="space-between">
					{isFetching || !profileData ? (
						<Loader size="sm" type="dots" />
					) : (
						`${profileData.firstName} ${profileData.lastName}`
					)}
				</Group>
				{links}
			</div>

			<Box className={classes.footer} p="xs">
				<Button
					onClick={handleLogout}
					variant="subtle"
					w="100%"
					leftSection={<IconLogout className={classes.linkIcon} stroke={1.5} />}
				>
					Logout
				</Button>
			</Box>
		</nav>
	);
};

export default UserNavbar;
