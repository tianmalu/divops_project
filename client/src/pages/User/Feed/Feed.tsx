import { Container, useMantineTheme } from "@mantine/core";
import { useInfiniteQuery } from "@tanstack/react-query";
import { useVirtualizer } from "@tanstack/react-virtual";
import React, { useEffect } from "react";
import Post from "./Post";

async function fetchServerPage(
	limit: number,
	offset: number = 0,
): Promise<{
	rows: Array<{ id: string; userMessage: string; aiMessage: string }>;
	nextOffset: number;
}> {
	const rows = new Array(limit).fill(0).map((_, i) => ({
		id: i.toString(),
		userMessage: "this is my prediction for today",
		aiMessage: "you will be lucky",
	}));

	await new Promise((r) => setTimeout(r, 500));

	return { rows, nextOffset: offset + 1 };
}

const Feed = () => {
	const theme = useMantineTheme();

	const {
		status,
		data,
		error,
		// isFetching,
		isFetchingNextPage,
		fetchNextPage,
		hasNextPage,
	} = useInfiniteQuery({
		queryKey: ["projects"],
		queryFn: (ctx) => fetchServerPage(10, ctx.pageParam),
		getNextPageParam: (lastGroup) => lastGroup.nextOffset,
		initialPageParam: 0,
	});

	const allRows = data ? data.pages.flatMap((d) => d.rows) : [];

	const parentRef = React.useRef<HTMLDivElement>(null);

	const rowVirtualizer = useVirtualizer({
		count: hasNextPage ? allRows.length + 1 : allRows.length,
		getScrollElement: () => parentRef.current,
		estimateSize: () => 200,
		overscan: 5,
	});

	useEffect(() => {
		const [lastItem] = [...rowVirtualizer.getVirtualItems()].reverse();

		if (!lastItem) {
			return;
		}

		if (
			lastItem.index >= allRows.length - 1 &&
			hasNextPage &&
			!isFetchingNextPage
		) {
			fetchNextPage();
		}
	}, [
		hasNextPage,
		fetchNextPage,
		allRows.length,
		isFetchingNextPage,
		rowVirtualizer,
	]);

	return (
		<Container
			fluid
			style={{
				border: `1px solid ${theme.colors.dark[4]}`,
				borderRadius: theme.radius.md,
				flex: 1,
				height: "calc(100vh - 32px)",
				padding: "10px",
			}}
		>
			<div>
				{status === "pending" ? (
					<p>Loading...</p>
				) : status === "error" ? (
					<span>Error: {error.message}</span>
				) : (
					<div
						ref={parentRef}
						className="List"
						style={{
							height: "calc(100vh - 52px)",

							width: `100%`,
							overflow: "auto",
						}}
					>
						<div
							style={{
								height: `${rowVirtualizer.getTotalSize()}px`,
								width: "100%",
								padding: "10px",
								position: "relative",
							}}
						>
							{rowVirtualizer.getVirtualItems().map((virtualRow) => {
								const isLoaderRow = virtualRow.index > allRows.length - 1;
								const post = allRows[virtualRow.index];

								return (
									<div
										key={virtualRow.index}
										className={
											virtualRow.index % 2 ? "ListItemOdd" : "ListItemEven"
										}
										style={{
											position: "absolute",
											top: 0,
											left: 0,
											width: "100%",
											height: `${virtualRow.size}px`,
											transform: `translateY(${virtualRow.start}px)`,
										}}
									>
										{isLoaderRow ? (
											hasNextPage ? (
												"Loading more..."
											) : (
												"Nothing more to load"
											)
										) : (
											<Post post={post} />
										)}
									</div>
								);
							})}
						</div>
					</div>
				)}
			</div>
		</Container>
	);
};

export default Feed;
