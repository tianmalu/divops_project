import { Box, Container, Group, Text, useMantineTheme } from "@mantine/core";
import type { Question } from "../../../api/discussions-api";

interface MessageProps {
	question: Question;
}

const Message = (props: MessageProps) => {
	const { question } = props;
	const theme = useMantineTheme();
	return (
		<Container fluid p="xs">
			<Group justify={question.fromUser ? "flex-end" : "flex-start"}>
				<Box
					p="md"
					maw="70%"
					bg="gray"
					style={{ borderRadius: theme.radius.lg }}
				>
					<Text size="sm">{question.text}</Text>
				</Box>
			</Group>
		</Container>
	);
};

export default Message;
