from taxii2client import Server, Collection

def fetch_threat_intelligence(taxii_server_url, collection_id):
    # Create a TAXII server object
    server = Server(taxii_server_url)

    try:
        # Discover available collections on the TAXII server
        collections = server.collections

        # Find the collection by ID
        collection = next((c for c in collections if c.id == collection_id), None)

        if collection:
            # Fetch STIX content from the specified collection
            objects = collection.get_objects()

            # Process the result
            for stix_object in objects:
                stix_data = stix_object.serialize(pretty=True)
                print(f"STIX Data:\n{stix_data}\n")
        else:
            print(f"Collection with ID '{collection_id}' not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the TAXII server URL
    taxii_server_url = 'https://your.taxii.server.com/taxii/'

    # Specify the collection ID you want to query
    collection_id = 'your_collection'

    # Fetch threat intelligence from the TAXII server
    fetch_threat_intelligence(taxii_server_url, collection_id)
