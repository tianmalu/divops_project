import {
	Avatar,
	Blockquote,
	Container,
	Group,
	Paper,
	Stack,
	Text,
} from "@mantine/core";
import classes from "./Post.module.css";

interface PostProps {
    post: {
        id: string;
        userMessage: string;
        aiMessage: string;
    }
}

const Post = (props: PostProps) => {
    const {post} = props;
	return (
		<Paper
			withBorder
			radius="md"
			className={classes.comment}
			p="lg"
			h="180px"
			py="10px"
		>
            <Container h="100%" fluid>
			<Group flex={1}>
				<Avatar
					src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png"
					alt="Jacob Warnhalter"
					radius="xl"
				/>
				<div>
					<Text fz="sm">Jacob Warnhalter</Text>
					<Text fz="xs" c="dimmed">
						10 minutes ago
					</Text>
				</div>
			</Group>
			
			<Stack flex={1}>
                {post.userMessage}
				<Blockquote p="xs">{post.aiMessage}</Blockquote>
			</Stack>
            </Container>
		</Paper>
	);
};

export default Post;
