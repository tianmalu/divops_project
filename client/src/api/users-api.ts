import { useMutation } from "@tanstack/react-query";
import { usersClient, type usersSchema } from "./clients";

export const UsersQueryKeys = {
	LOGIN: "LOGIN",
	REGISTER: "REGISTER",
};

interface UseLoginMutationProps {
	body: usersSchema["/api/users/login"]["post"]["requestBody"]["content"]["application/json"];
}

export function useLoginMutation({ body }: UseLoginMutationProps) {
	return useMutation({
		mutationKey: [UsersQueryKeys.LOGIN],
		mutationFn: () =>
			usersClient.POST("/api/users/login", {
				body,
			}),
	});
}

interface UseRegisterMutationProps {
	body: usersSchema["/api/users/register"]["post"]["requestBody"]["content"]["application/json"];
}

export function useRegisterMutation() {
	return useMutation({
		mutationKey: [UsersQueryKeys.REGISTER],
		mutationFn: ({ body }: UseRegisterMutationProps) =>
			usersClient.POST("/api/users/register", {
				body,
			}),
	});
}
