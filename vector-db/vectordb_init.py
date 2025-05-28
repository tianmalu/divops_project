import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
from weaviate.classes.config import Property, DataType, ReferenceProperty, AdditionalConfig, Timeout

import os
from dotenv import load_dotenv

import json
import pandas as pd
from weaviate.util import generate_uuid5
from tqdm import tqdm

load_dotenv()

weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
    skip_init_checks=True,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
    )
)

# print(client.is_ready())

# 1. KeywordMeaning
if not client.collections.exists("KeywordMeaning"):
    client.collections.create(
        name="KeywordMeaning",
        properties=[
            Property(name="keyword",      data_type=DataType.TEXT),
            Property(name="meaning",      data_type=DataType.TEXT),
            Property(name="feedback",     data_type=DataType.TEXT_ARRAY), 
            Property(name="source",       data_type=DataType.TEXT),
            Property(name="orientation",  data_type=DataType.TEXT),
            Property(name="position",     data_type=DataType.INT)
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_weaviate()
    )

# 2. TarotCard
if not client.collections.exists("TarotCard"):
    client.collections.create(
        name="TarotCard",
        properties=[
            Property(name="name", data_type=DataType.TEXT),
            Property(name="number", data_type=DataType.TEXT),
            Property(name="arcana", data_type=DataType.TEXT),
            Property(name="suit", data_type=DataType.TEXT),
            Property(name="img", data_type=DataType.TEXT),
            Property(name="fortune_telling", data_type=DataType.TEXT_ARRAY),
            Property(name="keywords", data_type=DataType.TEXT_ARRAY),
            Property(name="meanings_light", data_type=DataType.TEXT_ARRAY),
            Property(name="meanings_shadow", data_type=DataType.TEXT_ARRAY),
            Property(name="archetype", data_type=DataType.TEXT),
            Property(name="hebrew_alphabet", data_type=DataType.TEXT),
            Property(name="numerology", data_type=DataType.TEXT),
            Property(name="elemental", data_type=DataType.TEXT),
            Property(name="mythical_spiritual", data_type=DataType.TEXT),
            Property(name="questions_to_ask", data_type=DataType.TEXT_ARRAY)
        ],
        references=[
            ReferenceProperty(
                name="keywordsMeaning",
                target_collection="KeywordMeaning"
            )
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_weaviate()
    )

collections = client.collections.list_all()
#print(collections)
print("📦 Current Collections:")
for col_name in collections:
    print(f"- {col_name}")


# write basic data from json to the collections
data_url = "./tarot_images.json"
with open(data_url, "r") as f:
    data = json.load(f)

# Check if data is wrapped in a "cards" key
if isinstance(data, dict) and "cards" in data:
    cards_data = data["cards"]
else:
    cards_data = data
tarot_cards = client.collections.get("TarotCard")

with tarot_cards.batch.fixed_size(50) as batch:
    for card in tqdm(cards_data):
        card_obj = {
            "name": card.get("name", ""),
            "number": card.get("number", ""),
            "arcana": card.get("arcana", ""),
            "suit": card.get("suit", ""),
            "img": card.get("img", ""),
            "fortune_telling": card.get("fortune_telling", []),
            "keywords": card.get("keywords", []),
            "meanings_light": card.get("meanings", {}).get("light", []) if "meanings" in card else [],
            "meanings_shadow": card.get("meanings", {}).get("shadow", []) if "meanings" in card else [],
            "archetype": card.get("Archetype", ""),
            "hebrew_alphabet": card.get("Hebrew Alphabet", ""),
            "numerology": card.get("Numerology", ""),
            "elemental": card.get("Elemental", ""),
            "mythical_spiritual": card.get("Mythical/Spiritual", ""),
            "questions_to_ask": card.get("Questions to Ask", [])
        }
        batch.add_object(
            properties=card_obj,
            uuid=generate_uuid5(card["name"])
            # references=reference_obj  # You can add references here
        )
# Check for failures
if batch.number_errors > 0:
    print(f"⚠️ Finished with {batch.number_errors} errors")
else:
    print("✅ All cards imported successfully")

# Get the tarot collection
tarot = client.collections.get("TarotCard")
result = tarot.query.fetch_objects(limit=4)
for obj in result.objects:
    print(obj.properties)

client.close()
