import {
	ActionIcon,
	Box,
	Button,
	Center,
	Container,
	Divider,
	Group,
	Loader,
	ScrollArea,
	Space,
	Stack,
	Text,
	TextInput,
	Title,
	useMantineTheme,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { IconEdit, IconPlus } from "@tabler/icons-react";
import { useSearchParams } from "react-router-dom";
import AddDiscussionModal from "./AddDiscussionModal";
import Message from "./Message";
import TarotCard from "./TarotCard";

const discussions = [
	{ id: "1", title: "discussion long long long 1" },
	{ id: "2", title: "discussion 2" },
	{ id: "3", title: "discussion 3" },
	{ id: "4", title: "discussion 4" },
	{ id: "5", title: "discussion 5" },
	{ id: "6", title: "discussion long long long 1" },
	{ id: "7", title: "discussion 2" },
	{ id: "8", title: "discussion 3" },
	{ id: "9", title: "discussion 4" },
	{ id: "10", title: "discussion 5" },
	{ id: "11", title: "discussion 5" },
	{ id: "12", title: "discussion 5" },
	{ id: "13", title: "discussion 5" },
	{ id: "14", title: "discussion 5" },
	{ id: "15", title: "discussion 5" },
	{ id: "16", title: "discussion 5" },
	{ id: "17", title: "discussion 5" },
	{ id: "18", title: "discussion 5" },
];

const messages = [
	{
		id: "1",
		from: "user",
		text: "text from  usertext from  usertext from  usertext from  usertext from  usertext from  usertext from  usertext from  usertext from  usertext from  usertext from  usertext from  usertext from  user",
	},
	{ id: "2", from: "ai", text: "this is a reply from the ai agent " },
	{ id: "3", from: "user", text: "text from  user" },
	{ id: "4", from: "ai", text: "text from  user" },
	{ id: "5", from: "user", text: "text from  user" },
	{ id: "6", from: "ai", text: "text from  user" },
	{ id: "7", from: "user", text: "text from  user" },
];

interface DiscussionsListProps {
	openModal: VoidFunction;
}

const DiscussionsList = (props: DiscussionsListProps) => {
	const { openModal } = props;
	const theme = useMantineTheme();
	const [searchParams, setSearchParams] = useSearchParams();
	const discussionId = searchParams.get("discussionId");

	const handleDiscussionClicked = (d: { id: string; title: string }) => {
		console.log(d);
		setSearchParams({ discussionId: d.id });
	};

	return (
		<Stack
			h="100%"
			p="xs"
			maw="200px"
			style={{
				border: `1px solid ${theme.colors.dark[4]}`,
				borderRadius: theme.radius.md,
				flex: 1,
				flexGrow: 1,
			}}
		>
			<Group justify="space-between">
				<Title size="md">My Discussions </Title>
				<ActionIcon size="md" onClick={openModal}>
					<IconEdit />
				</ActionIcon>
			</Group>

			<Divider />
			<Container
				h="100%"
				w="100%"
				style={{
					flexGrow: "1",
				}}
			>
				<ScrollArea dir="column" h={550} offsetScrollbars flex={1}>
					<Stack>
						{discussions.map((d) => (
							<Button
								onClick={() => handleDiscussionClicked(d)}
								variant={discussionId === d.id ? "filled" : "subtle"}
								key={d.id}
								justify="flex-start"
							>
								<Text truncate="end" size="sm">
									{d.title}
								</Text>
							</Button>
						))}
					</Stack>
				</ScrollArea>
			</Container>
		</Stack>
	);
};

interface NoDiscussionSelectedProps {
	openModal: VoidFunction;
}

const NoDiscussionSelected = (props: NoDiscussionSelectedProps) => {
	const { openModal } = props;
	return (
		<Center h="100%" w="100%">
			<Stack w="70%" align="center" justify="center">
				{/* @ts-expect-error idk*/}
				<Title order={3} align="center">
					Please select a discussion or click below to create a new one!
				</Title>
				<Space h="sm" />
				<Button leftSection={<IconEdit />} size="md" onClick={openModal}>
					Create Discussion
				</Button>
			</Stack>
		</Center>
	);
};

const DiscussionMessages = () => {
	const [searchParams] = useSearchParams();
	const discussionId = searchParams.get("discussionId");
	console.log(discussionId);

	return (
		<Container
			fluid
			style={{
				height: "calc(100vh - 32px)",
				display: "flex",
				flexDirection: "column",
			}}
		>
			<Group grow>
				<TarotCard cardNumber="0" />
				<TarotCard cardNumber="1" />
				<TarotCard cardNumber="2" />
			</Group>
			<Box style={{ overflowY: "scroll" }}>
				{messages.map((m) => {
					return <Message key={m.id} message={m} />;
				})}
				<Loader type="dots"/>
			</Box>
			<Stack flex={1}>
				<Group grow mb="xs">
					<TextInput
						radius="md"
						placeholder="Write a message..."
						rightSection={
							<ActionIcon>
								<IconPlus />
							</ActionIcon>
						}
					/>
				</Group>
			</Stack>
		</Container>
	);
};

interface DiscussionMainScreenProps {
	openModal: VoidFunction;
	opened: boolean;
	closeModal: VoidFunction;
}

const DiscussionMainScreen = (props: DiscussionMainScreenProps) => {
	const { openModal, opened, closeModal } = props;
	const theme = useMantineTheme();
	const [searchParams] = useSearchParams();
	const discussionId = searchParams.get("discussionId");

	return (
		<Container
			fluid
			style={{
				border: `1px solid ${theme.colors.dark[4]}`,
				borderRadius: theme.radius.md,
				flex: 1,
				height: "calc(100vh - 32px)",
			}}
		>
			<AddDiscussionModal opened={opened} close={closeModal} />

			{discussionId ? (
				<DiscussionMessages />
			) : (
				<NoDiscussionSelected openModal={openModal} />
			)}
		</Container>
	);
};

const Discussions = () => {
	const [
		addDiscussionModalOpenen,
		{ open: openAddDiscussionModal, close: closeAddDiscussionModal },
	] = useDisclosure(false);
	return (
		<Group h="100%">
			<DiscussionsList openModal={openAddDiscussionModal} />
			<DiscussionMainScreen
				openModal={openAddDiscussionModal}
				opened={addDiscussionModalOpenen}
				closeModal={closeAddDiscussionModal}
			/>
		</Group>
	);
};

export default Discussions;
