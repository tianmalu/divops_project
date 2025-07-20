import { Button, Modal, Stack, TextInput } from "@mantine/core";
import { isNotEmpty, useForm } from "@mantine/form";
import { notifications } from "@mantine/notifications";
import { IconPlus } from "@tabler/icons-react";
import { useQueryClient } from "@tanstack/react-query";
import {
	DiscussionsQueryKeys,
	useAddDiscussionMutation,
} from "../../../api/discussions-api";

interface AddDiscussionModalProps {
	opened: boolean;
	close: VoidFunction;
}

interface AddDiscussionFormProps {
	name: string;
	text: string;
}

const AddDiscussionModal = (props: AddDiscussionModalProps) => {
	const { opened, close } = props;
	const queryClient = useQueryClient();
	const addDiscussionMutation = useAddDiscussionMutation();
	const form = useForm<AddDiscussionFormProps>({
		mode: "uncontrolled",
		initialValues: {
			name: "",
			text: "",
		},
		validate: {
			name: isNotEmpty("Required"),
			text: isNotEmpty("Required"),
		},
	});

	const closeModal = () => {
		form.reset();
		close();
	};

	const addDiscussion = async (values: AddDiscussionFormProps) => {
		try {
			await addDiscussionMutation.mutateAsync({
				body: values,
			});
			queryClient.invalidateQueries({
				queryKey: [DiscussionsQueryKeys.GET_DISCUSSIONS],
			});
			closeModal();
		} catch (e) {
			let message = "Unknown error";

			if (e instanceof Error) {
				message = e.message;
			}
			notifications.show({
				title: "Error creating a new discussion",
				message: message || "",
				color: "red",
				position: "top-right",
			});
		}
	};

	return (
		<Modal
			opened={opened}
			onClose={() => !addDiscussionMutation.isPending && closeModal()}
			title="Create New Discussion"
		>
			<form onSubmit={form.onSubmit(addDiscussion)}>
				<Stack>
					<TextInput
						withAsterisk
						label="Name"
						placeholder="bla bla"
						key={form.key("name")}
						{...form.getInputProps("name")}
						disabled={addDiscussionMutation.isPending}
					/>
					<TextInput
						withAsterisk
						label="Text"
						placeholder="bla bla"
						key={form.key("text")}
						{...form.getInputProps("text")}
						disabled={addDiscussionMutation.isPending}
					/>
					<Button
						leftSection={<IconPlus />}
						type="submit"
						disabled={addDiscussionMutation.isPending}
						loading={addDiscussionMutation.isPending}
					>
						Add Discussion
					</Button>
				</Stack>
			</form>
		</Modal>
	);
};

export default AddDiscussionModal;
