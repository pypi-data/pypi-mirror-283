from __future__ import annotations
import httpx
from .resource_abc import Resource
from typing import Dict, Any
from pydantic import BaseModel, Field

class SequenceResource(BaseModel, Resource):
    id: str = Field(exclude=True)
    scope: str
    code: str
    increment: int|None = None
    minValue: int|None = None
    maxValue: int|None = None
    start: int|None = None
    cycle: bool|None = None
    pattern: str|None = None

    def read(self, client, old_state) -> Dict[str, Any]:
        return client.request("get", f"/api/api/sequences/{self.scope}/{self.code}").json()

    def create(self, client: httpx.Client):
        desired = self.model_dump(mode="json", exclude_none=True)
        client.request("POST", f"/api/api/sequences/{self.scope}", json=desired)
        return {"scope": self.scope, "code": self.code}

    def update(self, client: httpx.Client, old_state):
        if [old_state.scope, old_state.code] != [self.scope, self.code]:
            raise (RuntimeError("Cannot change the scope/code on a sequence"))
        remote = self.read(client, old_state)
        desired = self.model_dump(mode="json", exclude_none=True, exclude={"scope","code"})
        effective = remote | desired
        if effective == remote:
            return None
        raise RuntimeError("Cannot modify a sequence")

    @staticmethod
    def delete(client, old_state):
        raise RuntimeError("Cannot delete a sequence")

    def deps(self):
        return []


