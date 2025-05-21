import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
from weaviate.classes.config import Property, DataType, ReferenceProperty

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
    skip_init_checks=True
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
            Property(name="name",            data_type=DataType.TEXT),
            Property(name="arcana",          data_type=DataType.TEXT),
            Property(name="suit",            data_type=DataType.TEXT),
            Property(name="uprightMeaning",  data_type=DataType.TEXT),
            Property(name="reversedMeaning", data_type=DataType.TEXT),
            Property(name="symbolism",       data_type=DataType.TEXT),
            Property(name="element",         data_type=DataType.TEXT),
            Property(name="astrology",       data_type=DataType.TEXT),
            Property(name="numerology",      data_type=DataType.TEXT),
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
data_url = "./card_basics.json"
with open(data_url, "r") as f:
    data = json.load(f)
df = pd.DataFrame(data)
tarot_cards = client.collections.get("TarotCard")

with tarot_cards.batch.fixed_size(50) as batch:
    for i, card in tqdm(df.iterrows()):
        card_obj = {
            "name": card["name"],
            "arcana": card["arcana"],
            "suit": card["suit"],
            "uprightMeaning": card["uprightMeaning"],
            "reversedMeaning": card["reversedMeaning"],
            "symbolism": card["symbolism"],
            "element": card["element"],
            "astrology": card["astrology"],
            "numerology": card["numerology"],
            "keywordsMeaning": []
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
result = tarot.query.fetch_objects(limit=10)
for obj in result.objects:
    print(obj.properties)

client.close()
