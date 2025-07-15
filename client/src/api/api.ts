import { useQuery } from "@tanstack/react-query";

enum QueryKeys {
	GET_DISCUSSIONS = "GET_DISCUSSIONS",
}

export function useGetDiscussionsQuery() {
	return useQuery({
		queryKey: [QueryKeys.GET_DISCUSSIONS],
	});
}
