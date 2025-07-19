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
import { isEmail, useForm } from "@mantine/form";
import { useNavigate } from "react-router";
import { useLoginMutation } from "../../../api/users-api";

interface LoginFormProps {
	email: string;
	password: string;
}

const Login = () => {
	const navigate = useNavigate();
	const loginMutation = useLoginMutation();
	const form = useForm<LoginFormProps>({
		mode: "uncontrolled",
		initialValues: {
			email: "",
			password: "",
		},
		validate: {
			email: isEmail("Invalid email"),
			password: (value) => (value ? null : "Password Required"),
		},
	});

	const login = async (values: LoginFormProps) => {
		try {
			const res = await loginMutation.mutateAsync({
				body: values,
			});
			if (res.data) {
				localStorage.setItem("token", res.data.token);
				navigate("/main");
			}
		} catch {
			// Nothing
		}
	};

	return (
		<Container size={420} my={40}>
			<form onSubmit={form.onSubmit(login)}>
				<Stack>
					<Title ta="center">Welcome back! Helm</Title>

					<Text ta="center">
						Do not have an account yet?{" "}
						<Anchor href="signup">Create account</Anchor>
					</Text>
				</Stack>

				<Paper withBorder shadow="sm" p={22} mt={30} radius="md">
					<Stack gap="sm">
						<TextInput
							withAsterisk
							label="Email"
							placeholder="your@email.com"
							key={form.key("email")}
							{...form.getInputProps("email")}
						/>
						<PasswordInput
							withAsterisk
							label="Password"
							placeholder="Your password"
							key={form.key("password")}
							{...form.getInputProps("password")}
						/>
						{loginMutation.isError && !loginMutation.isPending && (
							<Center>
								<Text color="red">{loginMutation.error.message}</Text>
							</Center>
						)}
						<Button type="submit" fullWidth mt="xl" radius="md">
							Sign in
						</Button>
					</Stack>
				</Paper>
			</form>
		</Container>
	);
};

export default Login;
