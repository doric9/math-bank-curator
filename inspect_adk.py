
import inspect
from google.adk import Agent

print("Agent class:", Agent)
print("\nAgent __init__ signature:", inspect.signature(Agent.__init__))
print("\nAgent fields (if pydantic):", getattr(Agent, 'model_fields', 'Not a Pydantic model'))
