import {
	Anchor,
	Button,
	Center,
	Container,
	Paper,
	PasswordInput,
	Stack,
	Text,
	TextInput,
	Title,
} from "@mantine/core";
import { isEmail, isNotEmpty, useForm } from "@mantine/form";
import { notifications } from "@mantine/notifications";
import { useNavigate } from "react-router";
import { useRegisterMutation } from "../../../api/users-api";

interface RegisterForm {
	firstName: string;
	lastName: string;
	email: string;
	password: string;
}

const Signup = () => {
	const navigate = useNavigate();
	const registerMutation = useRegisterMutation();

	const form = useForm<RegisterForm>({
		mode: "uncontrolled",
		initialValues: {
			firstName: "",
			lastName: "",
			email: "",
			password: "",
		},
		validate: {
			firstName: isNotEmpty("First Name Required"),
			lastName: isNotEmpty("Last Name Required"),
			email: isEmail("Invalid email"),
			password: isNotEmpty("Password Required"),
		},
	});

	const signup = async (values: RegisterForm) => {
		try {
			await registerMutation.mutateAsync({
				body: {
					firstName: values.firstName,
					lastName: values.lastName,
					email: values.email,
					password: values.password,
				},
			});

			notifications.show({
				title: "Account created successfully!",
				message: "You can now Log in",
				position: "top-right",
			});
			navigate("/signin");
		} catch {
			// Nothing
		}
	};

	return (
		<Container size={420} my={40}>
			<form onSubmit={form.onSubmit(signup)}>
				<Stack>
					<Title ta="center">Hello!</Title>

					<Text ta="center">
						Already have an account? <Anchor href="signin">Login</Anchor>
					</Text>
				</Stack>
				<Paper withBorder shadow="sm" p={22} mt={30} radius="md">
					<Stack gap="sm">
						<TextInput
							withAsterisk
							label="First Name"
							placeholder="John"
							key={form.key("firstName")}
							{...form.getInputProps("firstName")}
							disabled={registerMutation.isPending}
						/>
						<TextInput
							withAsterisk
							label="Last Name"
							placeholder="Doe"
							key={form.key("lastName")}
							{...form.getInputProps("lastName")}
							disabled={registerMutation.isPending}
						/>
						<TextInput
							withAsterisk
							label="Email"
							placeholder="your@email.com"
							key={form.key("email")}
							{...form.getInputProps("email")}
							disabled={registerMutation.isPending}
						/>
						<PasswordInput
							withAsterisk
							label="Password"
							placeholder="Your password"
							key={form.key("password")}
							{...form.getInputProps("password")}
							disabled={registerMutation.isPending}
						/>
						{registerMutation.isError && !registerMutation.isPending && (
							<Center>
								<Text color="red">{registerMutation.error.message}</Text>
							</Center>
						)}
						<Button
							type="submit"
							fullWidth
							mt="xl"
							radius="md"
							disabled={registerMutation.isPending}
							loading={registerMutation.isPending}
						>
							Sign Up
						</Button>
					</Stack>
				</Paper>
			</form>
		</Container>
	);
};

export default Signup;
