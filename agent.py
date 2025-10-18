import asyncio
from pathlib import Path

from fast_agent import FastAgent, RequestParams

fast = FastAgent("fast-agent example")


PROMPTS = Path(__file__).parent / "prompts"


@fast.agent(default=True)
@fast.agent(
    name="requirement_gatherer",
    instruction=PROMPTS / "requirement_gatherer.md",
    servers=["filesystem"],
)
@fast.agent(
    name="diagram_generator",
    instruction=PROMPTS / "diagram_generator.md",
    servers=["diagramming", "filesystem"],
)
@fast.agent(
    name="pitch_deck_generator",
    instruction=PROMPTS / "pitch_deck_generator.md",
    servers=["filesystem"],
)
@fast.agent(
    name="presentation_generator",
    instruction=PROMPTS / "presentation_generator.md",
    servers=["presentation", "filesystem"],
    request_params=RequestParams(max_iterations=51),
)
@fast.agent(
    name="github_agent",
    instruction="You are a helpful AI Agent",
    servers=["github_official", "github_direct_api", "filesystem"],
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
