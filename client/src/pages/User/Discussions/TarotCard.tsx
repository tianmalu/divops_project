import { Image } from "@mantine/core";
import cards from "../../../../public/tarot-images.json";

interface TarotCardProps {
	cardNumber: string;
}

const TarotCard = (props: TarotCardProps) => {
	const { cardNumber } = props;
	const card = cards.cards.find((c) => c.number === cardNumber);

	const imagePath = card ? `../../../../public/cards/${card.img}` : "";
	return <Image h={200} fit="contain" src={imagePath} />;
};

export default TarotCard;
