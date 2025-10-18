import os
import httpx
from mcp.server.fastmcp import FastMCP


mcp = FastMCP()
GITHUB_API_URL = "https://api.github.com/graphql"
AUTH_TOKEN = os.environ.get("GITHUB_TOKEN")


@mcp.tool()
async def query_github_api(query: str) -> dict:
    """
    Sends a GraphQL query to the GitHub API.

    Query is correctly wrapped in a JSON object.

    Example:

    query = `query{ node(id: \"PROJECT_ID\") { ... on ProjectV2 { fields(first: 20) { nodes { ... on ProjectV2FieldCommon { id name }}}}}}`
    curl command used:
    ```sh
    curl --request POST
        --url https://api.github.com/graphql \
        --header 'Authorization: Bearer TOKEN' \
        --data '{"query":"query{ node(id: \"PROJECT_ID\") { ... on ProjectV2 { fields(first: 20) { nodes { ... on ProjectV2FieldCommon { id name }}}}}}"}'
    ```
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_API_URL,
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            json={"query": query},
        )
        return response.json()


def main():
    mcp.run()


if __name__ == "__main__":
    main()
