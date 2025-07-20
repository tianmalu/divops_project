import { useMutation, useQuery } from "@tanstack/react-query";
import type { paths as discussionsPaths } from "../../discussions_service_types";
import { discussionsClient, type discussionsSchema } from "./clients";

export const DiscussionsQueryKeys = {
	GET_DISCUSSIONS: "GET_DISCUSSIONS",
	GET_DISCUSSION_DETAILS: "GET_DISCUSSION_DETAILS",
	ADD_DISCUSSION: "ADD_DISCUSSION",
	ADD_QUESTION: "ADD_QUESTION",
};

export type Discussion =
	discussionsPaths["/api/discussions/discussions"]["get"]["responses"]["200"]["content"]["*/*"]["data"][number];
export type Question =
	discussionsPaths["/api/discussions/discussion"]["get"]["responses"]["200"]["content"]["*/*"]["questions"][number];

export function useGetDiscussions() {
	return useQuery({
		queryKey: [DiscussionsQueryKeys.GET_DISCUSSIONS],
		queryFn: async () => {
			const res = await discussionsClient.GET("/api/discussions/discussions");
			return res.data;
		},
	});
}

interface UseGetDiscussionDetailsProps {
	discussionId: string | null;
}

export function useGetDiscussionDetails({
	discussionId,
}: UseGetDiscussionDetailsProps) {
	return useQuery({
		queryKey: [DiscussionsQueryKeys.GET_DISCUSSION_DETAILS,{discussionId}],
		enabled: !!discussionId,
		queryFn: async () => {
			const res = await discussionsClient.GET("/api/discussions/discussion", {
				params: {
					query: {
						discussionId: discussionId || "",
					},
				},
			});
			return res.data;
		},
	});
}

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

interface UseAddQuestionMutationProps {
	body: discussionsSchema["/api/discussions/question"]["post"]["requestBody"]["content"]["application/json"];
}

export function useAddQuestionMutation() {
	return useMutation({
		mutationKey: [DiscussionsQueryKeys.ADD_QUESTION],
		mutationFn: ({ body }: UseAddQuestionMutationProps) =>
			discussionsClient.POST("/api/discussions/question", {
				body,
			}),
	});
}
