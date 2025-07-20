import { useMutation, useQuery } from "@tanstack/react-query";
import { discussionsClient, type discussionsSchema } from "./clients";

export const DiscussionsQueryKeys = {
	GET_DISCUSSIONS: "GET_DISCUSSIONS",
	ADD_DISCUSSION: "ADD_DISCUSSION",
};

// export function useGetDiscussions() {
// 	return useQuery({
// 		queryKey: [DiscussionsQueryKeys.GET_DISCUSSIONS],
// 		queryFn: async () => {
// 			const res = await discussionsClient.GET("/api/users/profile");
// 			return res.data;
// 		},
// 	});
// }

interface UseAddDiscussionMutationProps {
	body: discussionsSchema["/api/discussions/discussion"]["post"]["requestBody"]["content"]["application/json"];
}

export function useAddDiscussionMutation() {
	return useMutation({
		mutationKey: [DiscussionsQueryKeys.ADD_DISCUSSION],
		mutationFn: ({ body }: UseAddDiscussionMutationProps) =>
			discussionsClient.POST("/api/discussions/discussion", {
				body,
			}),
	});
}

// interface UseRegisterMutationProps {
// 	body: usersSchema["/api/users/register"]["post"]["requestBody"]["content"]["application/json"];
// }

// export function useRegisterMutation() {
// 	return useMutation({
// 		mutationKey: [UsersQueryKeys.REGISTER],
// 		mutationFn: ({ body }: UseRegisterMutationProps) =>
// 			usersClient.POST("/api/users/register", {
// 				body,
// 			}),
// 	});
// }
