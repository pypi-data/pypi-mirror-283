#!/usr/bin/env python3

import os

from jmapc import Client
from jmapc.methods import IdentityGet, IdentityGetResponse

# Create and configure client
client = Client.create_with_api_token(
    host=os.environ["JMAP_HOST"], api_token=os.environ["JMAP_API_TOKEN"]
)

# Prepare Identity/get request
# To retrieve all of the user's identities, no arguments are required.
method = IdentityGet()

# Call JMAP API with the prepared request
result = client.request(method)

# Print some information about each retrieved identity
assert isinstance(result, IdentityGetResponse), "Error in Identity/get method"
for identity in result.data:
    print(
        f"Identity {identity.id} is for "
        f"{identity.name} at {identity.email}"
    )

# Example output:
#
# Identity 12345 is for Ness at ness@onett.example.com
# Identity 67890 is for Ness at ness-alternate@onett.example.com
