import { Button, Modal, Stack, TextInput } from "@mantine/core";
import { isNotEmpty, useForm } from "@mantine/form";
import { IconPlus } from "@tabler/icons-react";

interface AddDiscussionModalProps {
	opened: boolean;
	close: VoidFunction;
}

interface AddDiscussionFormProps {
	title: string;
}

const AddDiscussionModal = (props: AddDiscussionModalProps) => {
	const { opened, close } = props;
	const form = useForm<AddDiscussionFormProps>({
		mode: "uncontrolled",
		initialValues: {
			title: "",
		},
		validate: {
			title: isNotEmpty("Required"),
		},
	});

	const addDiscussion = (values: AddDiscussionFormProps) => {
		console.log(values);
	};

	return (
		<Modal opened={opened} onClose={close} title="Create New Discussion">
			<form onSubmit={form.onSubmit(addDiscussion)}>
				<Stack>
					<TextInput
						withAsterisk
						label="Title"
						placeholder="bla bla"
						key={form.key("title")}
						{...form.getInputProps("title")}
					/>
					<Button leftSection={<IconPlus />} type="submit">
						Add Discussion
					</Button>
				</Stack>
			</form>
		</Modal>
	);
};

export default AddDiscussionModal;
