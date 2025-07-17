import { Box, Container, Group, Text, useMantineTheme } from "@mantine/core";

interface MessageProps {
	message: {
		id: string;
		from: string;
		text: string;
	};
}

const Message = (props: MessageProps) => {
	const { message } = props;
	const theme = useMantineTheme();
	return (
		<Container fluid p="xs">
			<Group justify={message.from === "user" ? "flex-end" : "flex-start"}>
				<Box
					p="md"
					maw="70%"
					bg="gray"
					style={{ borderRadius: theme.radius.lg }}
				>
					<Text size="sm">{message.text}</Text>
				</Box>
			</Group>
		</Container>
	);
};

export default Message;
