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
import { isNotEmpty, useForm } from "@mantine/form";
import { useDisclosure } from "@mantine/hooks";
import { notifications } from "@mantine/notifications";
import { IconEdit, IconPlus } from "@tabler/icons-react";
import { useQueryClient } from "@tanstack/react-query";
import { useSearchParams } from "react-router-dom";
import {
	type Discussion,
	DiscussionsQueryKeys,
	useAddQuestionMutation,
	useGetDiscussionDetails,
	useGetDiscussions,
} from "../../../api/discussions-api";
import AddDiscussionModal from "./AddDiscussionModal";
import Message from "./Message";
import TarotCard from "./TarotCard";

interface DiscussionsListProps {
	openModal: VoidFunction;
}

const DiscussionsList = (props: DiscussionsListProps) => {
	const { openModal } = props;
	const theme = useMantineTheme();
	const { data, isFetching } = useGetDiscussions();
	const [searchParams, setSearchParams] = useSearchParams();
	const discussionId = searchParams.get("discussionId");

	const handleDiscussionClicked = (d: Discussion) => {
		setSearchParams({ discussionId: d.id.toString() });
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
					{isFetching ? (
						<Center>
							<Loader size="lg" />
						</Center>
					) : !data?.data || data.data.length === 0 ? (
						<Center>
							<Text>No Discussions </Text>
						</Center>
					) : (
						<Stack>
							{data.data.map((d) => (
								<Button
									onClick={() => handleDiscussionClicked(d)}
									variant={
										discussionId === d.id.toString() ? "filled" : "subtle"
									}
									key={d.id}
									justify="flex-start"
								>
									<Text truncate="end" size="sm">
										{d.name}
									</Text>
								</Button>
							))}
						</Stack>
					)}
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

interface AddQuestionForm {
	text: string;
}

const DiscussionMessages = () => {
	const [searchParams] = useSearchParams();
	const discussionId = searchParams.get("discussionId");
	const queryClient = useQueryClient();
	const addQuestionMutation = useAddQuestionMutation();
	const { data, isLoading } = useGetDiscussionDetails({ discussionId });
	const questions = data?.questions || [];
	const cards = (data?.cards || "").split(",");

	const form = useForm<AddQuestionForm>({
		mode: "uncontrolled",
		initialValues: {
			text: "",
		},
		validate: {
			text: isNotEmpty("Text Required"),
		},
	});

	const addQuestion = async (values: AddQuestionForm) => {
		try {
			await addQuestionMutation.mutateAsync({
				body: {
					discussionId: discussionId || "",
					text: values.text,
				},
			});

			queryClient.invalidateQueries({
				queryKey: [DiscussionsQueryKeys.GET_DISCUSSION_DETAILS],
			});
			form.reset();
		} catch (e) {
			let message = "Unknown error";

			if (e instanceof Error) {
				message = e.message;
			}
			notifications.show({
				title: "Error adding a new message",
				message: message || "",
				color: "red",
				position: "top-right",
			});
		}
	};

	return (
		<Container
			fluid
			style={{
				height: "calc(100vh - 32px)",
				display: "flex",
				flexDirection: "column",
			}}
		>
			<Group grow pb="xs">
				{cards.map((c) => (
					<TarotCard key={c} cardName={c} />
				))}
			</Group>
			{isLoading ? (
				<Center>
					<Loader size="lg" />
				</Center>
			) : (
				<Box style={{ overflowY: "scroll" }}>
					{questions.map((q) => {
						return <Message key={q.id.toString()} question={q} />;
					})}
					{addQuestionMutation.isPending && <Loader type="dots" />}
				</Box>
			)}
			<Stack flex={1}>
				<form onSubmit={form.onSubmit(addQuestion)}>
					<Group grow mb="xs">
						<TextInput
							key={form.key("text")}
							{...form.getInputProps("text")}
							disabled={isLoading || addQuestionMutation.isPending}
							radius="md"
							placeholder="Write a message..."
							rightSection={
								<ActionIcon>
									<IconPlus />
								</ActionIcon>
							}
						/>
					</Group>
				</form>
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
