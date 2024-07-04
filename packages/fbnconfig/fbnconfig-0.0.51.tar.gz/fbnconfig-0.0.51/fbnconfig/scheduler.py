import subprocess
import json
import copy
from . import configuration as cfg
from . import identity
from httpx import Client, HTTPStatusError
from .resource_abc import Resource, Ref
from typing import Optional, Dict, Any, Union, Literal, List
from datetime import datetime
import time
from pydantic import BaseModel, computed_field, field_serializer, Field


class ImageRef(BaseModel, Ref):
    """Reference an existing image
    Example
    -------
    >>> from fbnconfig.scheduler import ImageRef
    >>> image_ref = ImageRef(dest_name="myimage", dest_tag="0.1.1")
    """
    id: str
    dest_name: str
    dest_tag: str

    def attach(self, client):
        # we only need to check it exists
        client.get(f"/scheduler2/api/images/{self.dest_name}:{self.dest_tag}")


class ImageResource(BaseModel, Resource):
    """Define an image

    Example
    -------
    >>> from fbnconfig.scheduler import ImageResource
    >>> image = ImageResource(
            id="img1",
            source_image="docker.io/alpine:3.16.7",
            dest_name="myimage",
            dest_tag="3.16.7")
    """
    id: str
    source_image: str
    dest_name: str
    dest_tag: str

    def read(self, client, old_state):
        pass

    def create(self, client):
        env_name = client.base_url.host.split(".")[0]

        downstream_image = f"{client.base_url.host}/{env_name}/{self.dest_name}:{self.dest_tag}"

        # pull from the upstream and apply the downstream tag
        pull_commands = self._pull_commands(downstream_image)

        for cmd in pull_commands:
            subprocess.run(cmd).check_returncode()
        # get local and downstream digests to see if they match
        local_digest = self._getLocalDigest(downstream_image)

        if local_digest is not None:
            downstream_images = self._getRemoteTags(client, self.dest_name, local_digest)
            matching_tag = next((tag for tag in downstream_images if tag["name"] == self.dest_tag), None)
            if matching_tag is not None:  # this image/tag combo already exists
                print("image already exists in the remote with the same digest")
                return {
                    "id": self.id,
                    "source_image": self.source_image,
                    "dest_name": self.dest_name,
                    "dest_tag": self.dest_tag,
                }
        # create a unique tag so scheduler will give us auth info and not complain about
        # reusing an existing one
        body = {"imageName": f"{self.dest_name}:{time.time()}"}
        upload = client.post("/scheduler2/api/images", json=body)
        auth = upload.json()["dockerLoginCommand"].split(" ")

        # push the tag we actually want to have using the auth from scheduler
        push_commands = self._push_commands(downstream_image, auth)

        for cmd in push_commands:
            subprocess.run(cmd).check_returncode()

        return {
            "id": self.id,
            "source_image": self.source_image,
            "dest_name": self.dest_name,
            "dest_tag": self.dest_tag,
        }

    def _getRemoteTags(self, client, dest_name, local_digest):
        repo = client.get(f"/scheduler2/api/images/repository/{dest_name}")
        # todo: this could be paged
        return next(
            (img["tags"] for img in repo.json()["values"] if img["digest"] == local_digest),
            [],
        )

    def _getLocalDigest(self, tag):
        inspect = subprocess.run(
            ["docker", "inspect", "--format", "{{json .RepoDigests}}", tag],
            capture_output=True,
            text=True,
        )
        inspect.check_returncode()
        # inspect returns:
        #   [alpine@sha256:a8cb.. fbn-qa.lusid.com/fbn-qa/beany@sha256:b797...]
        repo = tag.split(":")[0]
        return next(
            (
                digest.split("@")[1]
                for digest in json.loads(inspect.stdout)
                if digest.split("@")[0] == repo
            ),
            None,
        )

    def _push_commands(self, tag, auth):
        return [
            ["docker", "login", "-u", auth[3], "--password", auth[5], auth[6]],
            ["docker", "push", tag],
        ]

    def _pull_commands(self, tag):
        return [
            ["docker", "pull", "--platform", "linux/amd64", self.source_image],
            ["docker", "tag", self.source_image, tag],
        ]

    def update(self, client, old_state):
        if (
            self.source_image == old_state.source_image
            and self.dest_name == old_state.dest_name
            and self.dest_tag == old_state.dest_tag
        ):
            return None
        return self.create(client)

    @staticmethod
    def delete(client, old_state):
        # no delete for images
        pass

    def deps(self):
        return []

class CommandlineArg(BaseModel):
    """Define a commandline ArgumentDefinition for a JobResource"""
    dataType: Literal["String", "Int"]
    required: Optional[bool] = False
    description: str
    order: int
    passedAs: Literal["CommandLine"] = "CommandLine"
    defaultValue: None|str = None

class EnvironmentArg(BaseModel):
    """Define a environment ArgumentDefinition for a JobResource"""
    dataType: Literal["String", "Int", "SecureString", "Configuration"]
    required: Optional[bool] = False
    description: str
    order: int
    passedAs: Literal["EnvironmentVariable"] = "EnvironmentVariable"
    defaultValue: None|str|cfg.ItemRef|cfg.ItemResource = None

    @field_serializer("defaultValue", when_used="always")
    def value_ser(self, value) -> str|None:
        if value is None:
            return None
        if isinstance(value, (cfg.ItemRef, cfg.ItemResource)):
            return value.ref
        return value

class JobRef(BaseModel, Ref):
    """Reference an existing scheduler job"""
    id: str = Field(exclude=True)
    scope: str
    code: str

    def attach(self, client):
        # just check it exists
        search = client.request(
            "get",
            "/scheduler2/api/jobs",
            params={"filter": f"jobId.scope eq '{self.scope}' and jobId.code eq '{self.code}'"},
        )

        current = next((job for job in search.json()["values"]), None)
        if current is None:
            raise RuntimeError(
                f"Failed to attach JobRef to job with scope={self.scope} and code={self.code}"
            )


class JobState(BaseModel):
    id: str
    scope: str
    code: str


class JobResource(BaseModel, Resource):
    """Manage a JobDefinition"""
    id: str = Field(exclude=True)
    scope: str = Field(exclude=True, init=True)
    code: str = Field(exclude=True, init=True)
    image: Union[ImageResource, ImageRef] = Field(exclude=True, init=True)
    name: str
    author: Optional[str] = None
    dateCreated: Optional[datetime] = None
    description: str
    ttl: Optional[int] = None
    minCpu: Optional[str] = None
    maxCpu: Optional[str] = None
    minMemory: Optional[str] = None
    maxMemory: Optional[str] = None
    argumentDefinitions: Dict[str, CommandlineArg|EnvironmentArg] = {}
    commandLineArgumentSeparator: Optional[str] = None
    remote: Dict[str, Any] = Field({}, exclude=True, init=False)

    @computed_field
    def jobId(self) -> Dict[str, str]:
        return {"scope": self.scope, "code": self.code}

    @computed_field
    def imageName(self) -> str:
        return self.image.dest_name

    @computed_field
    def imageTag(self) -> str:
        return self.image.dest_tag

    def read(self, client: Client, old_state):
        search = client.get(
            "/scheduler2/api/jobs",
            params={
                "filter": f"jobId.scope eq '{old_state.scope}' and jobId.code eq '{old_state.code}'"
            },
        )
        current = next(job for job in search.json()["values"])
        # normalise the current values
        current.pop("jobId")
        current.pop("requiredResources")
        current["imageName"] = current["dockerImage"].split(":")[
            0
        ]  # we get dockerImage but have to send separately :(
        current["imageTag"] = current["dockerImage"].split(":")[1]
        current.pop("dockerImage")
        self.remote = current

    def create(self, client):
        desired = self.model_dump(mode="json", exclude_none=True)
        client.post("/scheduler2/api/jobs", json=desired)
        newState = JobState(
            id=self.id,
            scope=self.scope,
            code=self.code
        )
        return newState.model_dump()

    def update(self, client: Client, old_state):
        if self.scope != old_state.scope or self.code != old_state.code:
            raise (RuntimeError("Cannot change identifier on job. Create a new one"))
        self.read(client, old_state)
        remote = copy.deepcopy(self.remote)
        desired = self.model_dump(mode="json", exclude_none=True, exclude={"jobId"})
        effective = remote | desired
        remoteArgs = remote["argumentDefinitions"]
        effectiveArgs = {
            argKey: remoteArgs.get(argKey, {}) | argValue
            for argKey, argValue in desired["argumentDefinitions"].items()
        }
        effective["argumentDefinitions"] = effectiveArgs
        if effective == remote:
            return None
        client.put(f"/scheduler2/api/jobs/{self.scope}/{self.code}", json=desired)
        new_state = JobState(
            id=self.id,
            scope=self.scope,
            code=self.code
        )
        return new_state.model_dump()

    @staticmethod
    def delete(client: Client, old_state):
        client.delete(f"/scheduler2/api/jobs/{old_state.scope}/{old_state.code}")

    def cleanup(self, client, oldState):
        if self.scope != oldState.scope or self.code != oldState.code:
            return self.delete(client, oldState)
        return None

    def deps(self):
        config_args: List[cfg.ItemRef|cfg.ItemResource] = [
            arg.defaultValue for arg in self.argumentDefinitions.values()
            if isinstance(arg.defaultValue, (cfg.ItemRef, cfg.ItemResource))
        ]
        return [self.image] + config_args


class ScheduleState(BaseModel):
    id: str
    scope: str
    code: str
    argKeys: List[str]


class ScheduleResource(BaseModel, Resource):
    """Manage a ScheduleDefinition"""
    id: str = Field(exclude=True)
    name: str
    scope: str = Field(exclude=True, init=True)
    code: str = Field(exclude=True, init=True)
    expression: str = Field(exclude=True, init=True)
    timezone: str = Field(exclude=True, init=True)
    job: JobResource | JobRef = Field(serialization_alias="jobId")
    description: str
    author: Optional[str] = None
    owner: Optional[str] = None
    arguments: None | Dict[str, str|cfg.ItemResource|cfg.ItemRef] = None
    enabled: Optional[bool] = None
    useAsAuth: identity.UserResource | identity.UserRef | None = None
    _remote: Dict[str, Any] = {}

    @field_serializer("useAsAuth", when_used="always")
    def serialize_auth(self, user: identity.UserResource | identity.UserRef | None = None):
        return user.userId if user else None

    @field_serializer("arguments", when_used="always")
    def serialize_args(self, args) -> Dict[str, str]:
        return {
            k: v.ref if isinstance(v, (cfg.ItemRef, cfg.ItemResource)) else v
            for k,v in args.items()
        }

    @field_serializer("job", when_used="always",)
    def serialize_job(self, job: JobResource | JobRef):
        return {"scope": job.scope, "code": job.code}

    @computed_field
    def scheduleId(self) -> Dict[str, str]:
        return {"scope": self.scope, "code": self.code}

    @computed_field
    def trigger(self) -> Dict[str, Dict[str,str]]:
        return {
            "timeTrigger": {
                "expression": self.expression,
                "timeZone": self.timezone,
            }
        }

    def read(self, client, old_state):
        get = client.get(f"/scheduler2/api/schedules/{old_state.scope}/{old_state.code}")
        current = get.json()
        # note scheduleId for create scheduleIdentifier for read :(
        current.pop("scheduleIdentifier")
        self._remote = current

    def create(self, client):
        body = self.model_dump(mode="json", exclude_none=True, by_alias=True)
        client.post("/scheduler2/api/schedules", json=body)
        arg_keys = list(self.arguments.keys()) if self.arguments else []
        return ScheduleState(id=self.id, scope=self.scope, code=self.code, argKeys=arg_keys).model_dump()

    def update(self, client, old_state):
        if self.scope != old_state.scope or self.code != old_state.code:
            from_id = f"{old_state.scope}/{old_state.code}"
            to_id = f"{self.scope}/{self.code}"
            raise (RuntimeError(f"Cannot change schedule identifier. From: '{from_id}', to: '{to_id}'"))
        self.read(client, old_state)
        remote = copy.deepcopy(self._remote)
        desired = self.model_dump(mode="json", exclude_none=True, by_alias=True, exclude={"scheduleId"})
        effective = remote | desired
        # On read the schedule will contain schedule args and args from the job.
        # Only update if the user specified args are different to the remote
        effective["arguments"] = remote.get("arguments", {}) | desired.get("arguments", {})
        arg_keys = list(self.arguments.keys()) if self.arguments else []
        if effective == remote and arg_keys == getattr(old_state, "argKeys", []):
            return None
        client.put(f"/scheduler2/api/schedules/{self.scope}/{self.code}", json=desired)
        return ScheduleState(id=self.id, scope=self.scope, code=self.code, argKeys=arg_keys).model_dump()

    @staticmethod
    def delete(client, old_state):
        try:
            client.delete(f"/scheduler2/api/schedules/{old_state.scope}/{old_state.code}")
        except HTTPStatusError as ex:
            content = ex.response.json()
            if (
                ex.response.status_code == 404
                and content.get("name", None) == "ValidationError"
                and content.get("title", None) == "Schedule could not be found"
            ):
                pass
            else:
                raise ex

    def cleanup(self, client, old_state):
        if self.scope != old_state.scope or self.code != old_state.code:
            return self.delete(client, old_state)
        return None

    def deps(self):
        config_args: List[cfg.ItemRef|cfg.ItemResource] = [
            value for value in self.arguments.values()
            if isinstance(value, (cfg.ItemRef, cfg.ItemResource))
        ] if self.arguments else []
        return [self.job] + config_args
