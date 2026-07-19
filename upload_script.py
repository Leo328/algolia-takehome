import json
from algoliasearch.search.client import SearchClientSync

DATA_FILE = 'data.json'
ALGOLIA_APP_ID= ""
ALGOLIA_API_KEY=""
ALGOLIA_INDEX_NAME="products"

def load_data(data=DATA_FILE):
    with open(data, 'r', encoding='utf-8') as f:
        parsed_data = json.load(f)
    return parsed_data


def count_data(data):
    count = len(data)
    print(f"Total number of objects: {count}")
    return count


def validate_object_ids(data):
    seen_ids = set()
    for position, record in enumerate(data):
        object_id = record.get("objectID")

        if object_id and object_id not in seen_ids:
            seen_ids.add(object_id)
        elif object_id and object_id in seen_ids:
            raise ValueError(
                f"Record at position {position} has a duplicate objectID."
            )
        elif object_id is None or object_id.strip() == "":
            raise ValueError(
                f"Record at position {position} does not have a valid objectID."
            )
    return True


def upload_to_algolia(data, app_id=ALGOLIA_APP_ID, api_key=ALGOLIA_API_KEY, index_name=ALGOLIA_INDEX_NAME):
    client = SearchClientSync(app_id=app_id, api_key=api_key,)

    try:
        responses = client.save_objects(index_name=index_name,  objects=data, wait_for_tasks=True)
    finally:
        client.close()

    print(
        f"Successfully uploaded {len(data)} records "
        f"to the '{index_name}' index."
    )
    return responses

def main():
    data = load_data()
    print(f"Loaded {len(data)} records from {DATA_FILE}.")

    validate_object_ids(data)

    upload_to_algolia(
        data=data,
        app_id=ALGOLIA_APP_ID,
        api_key=ALGOLIA_API_KEY,
        index_name=ALGOLIA_INDEX_NAME,
    )

if __name__ == "__main__":
    main()
