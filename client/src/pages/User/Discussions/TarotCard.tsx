import { Image } from "@mantine/core";
import cards from "./tarot-images.json";

interface TarotCardProps {
	cardName: string;
}

const TarotCard = (props: TarotCardProps) => {
	const { cardName } = props;
	const card = cards.cards.find((c) => c.name === cardName);

	const imagePath = card ? `/cards/${card.img}` : "";
	return <Image h={200} fit="contain" src={imagePath} />;
};

export default TarotCard;
