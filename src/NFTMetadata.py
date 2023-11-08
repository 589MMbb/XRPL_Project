import json
import os

# Assuming 'air_rights_output.json' and 'building_data.json' are in the current directory
AIR_RIGHTS_OUTPUT_JSON_PATH = "air_rights_output.json"
BUILDING_DATA_JSON_PATH = "building_data.json"
COMBINED_NFT_METADATA_JSON_PATH = "CombinedNFTMetadata.json"

# Load the air rights data
with open(AIR_RIGHTS_OUTPUT_JSON_PATH, 'r') as file:
    air_rights_data = json.load(file)

# Load the building data
with open(BUILDING_DATA_JSON_PATH, 'r') as file:
    building_data = json.load(file)

# Combine the data
building_name = air_rights_data["building"]
if building_name in building_data:
    combined_data = {
        "building": building_name,
        "air_rights_data": air_rights_data["air_rights_value"],
        "building_data": building_data[building_name],
        "sample_nft_uri": f"ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf4dfuylqabf3oclgtqy55fbzdi/{building_name}.json"
    }

# Write the combined data to a JSON file
with open(COMBINED_NFT_METADATA_JSON_PATH, 'w') as file:
    json.dump(combined_data, file, indent=4)

print(f"Combined NFT metadata saved to {COMBINED_NFT_METADATA_JSON_PATH}")

