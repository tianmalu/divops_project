import { useMutation, useQuery } from "@tanstack/react-query";
import { usersClient, type usersSchema } from "./clients";

export const UsersQueryKeys = {
	GET_USER_PROFILE: "GET_USER_PROFILE",
	LOGIN: "LOGIN",
	REGISTER: "REGISTER",
};

export function useGetUserProfile() {
	return useQuery({
		queryKey: [UsersQueryKeys.GET_USER_PROFILE],
		queryFn: async () => {
			const res = await usersClient.GET("/api/users/profile");
			return res.data;
		},
	});
}

interface UseLoginMutationProps {
	body: usersSchema["/api/users/login"]["post"]["requestBody"]["content"]["application/json"];
}

export function useLoginMutation() {
	return useMutation({
		mutationKey: [UsersQueryKeys.LOGIN],
		mutationFn: ({ body }: UseLoginMutationProps) =>
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
