# Saola GraphQL API client

This is a GraphQL client for Python based on the `ariadne-codegen` pip package. It is used to access the API at [app.saola.sg](https://app.saola.sg).

The client provides a convenient way to interact with the Saola GraphQL API, allowing you to perform various queries and mutations related to users, connections, workspaces, chats, and sources.

To add more queries and mutations, you can create new files with the `.graphql` extension in the `saola_graphql_client/graphql` directory. Once you have added your new GraphQL files, run the `./saola_graphql_client/run-codegen.sh` script to generate the necessary client code.

### Installation

```bash
pip install saola-graphql-client
```

### Usage

To use the client, you can import the generated client class and use it to perform queries and mutations. Here is an example:

```python
import asyncio
import jwt
from saola_graphql_client.graphql_client import Client as SaolaGraphQLClient

access_token = "your_access_token"
jwt_payload = jwt.decode(access_token, options={"verify_signature": False})
user_id = jwt_payload.get("hasura", {}).get("x-hasura-user-id")

client = SaolaGraphQLClient(
    url="https://app.saola.sg/v1/graphql",
    headers={"Authorization": f"Bearer {access_token}"},
)


async def get_and_print_current_user(client, user_id):
    current_user = await client.get_user(id=user_id)
    print(current_user)


asyncio.run(get_and_print_current_user(client, user_id))
```

Check `examples/` for more examples.


### Available methods

Check [saola_graphql_client/graphql_client/client.py](saola_graphql_client/graphql_client/client.py) for the available methods.
