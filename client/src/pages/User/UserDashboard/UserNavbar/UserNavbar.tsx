import { Box, Button, Group } from "@mantine/core";
import { IconBellRinging, IconLogout } from "@tabler/icons-react";
import { useState } from "react";
import { useNavigate } from "react-router";
import classes from "./UserNavbar.module.css";

const data = [
	{ link: "discussions", label: "Discussions", icon: IconBellRinging },
	{ link: "feed", label: "Feed", icon: IconBellRinging },
];

const UserNavbar = () => {
	const navigate = useNavigate();
	const [active, setActive] = useState("Billing");

	const links = data.map((item, idx) => (
		<Button
			justify="flex-start"
			w="100%"
			variant={item.label === active ? "default" : "transparent"}
			leftSection={<item.icon className={classes.linkIcon} stroke={1.5} />}
			key={idx}
			onClick={() => {
				setActive(item.label);
				navigate(item.link);
			}}
		>
			{item.label}
		</Button>
	));

	const handleLogout = () => {
		console.log("Handle logout");
	};

	return (
		<nav className={classes.navbar}>
			<div className={classes.navbarMain}>
				<Group className={classes.header} justify="space-between">
					User Name
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
