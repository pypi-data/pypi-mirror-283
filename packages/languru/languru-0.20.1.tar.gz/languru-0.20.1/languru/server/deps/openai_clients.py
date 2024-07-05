import time
from logging import Logger
from typing import Any, List, Optional, Text, Union

from fastapi import Query, Request
from openai import AzureOpenAI, OpenAI, OpenAIError
from openai.types import Model

from languru.config import logger as languru_logger
from languru.exceptions import (
    CredentialsNotProvided,
    ModelNotFound,
    OrganizationNotFound,
)
from languru.openai_plugins.clients.anthropic import AnthropicOpenAI
from languru.openai_plugins.clients.google import GoogleOpenAI
from languru.openai_plugins.clients.groq import GroqOpenAI
from languru.openai_plugins.clients.pplx import PerplexityOpenAI
from languru.openai_plugins.clients.voyage import VoyageOpenAI
from languru.server.utils.common import get_value_from_app
from languru.types.models import (
    MODELS_ANTHROPIC,
    MODELS_AZURE_OPENAI,
    MODELS_GOOGLE,
    MODELS_GROQ,
    MODELS_OPENAI,
    MODELS_PERPLEXITY,
    MODELS_VOYAGE,
)
from languru.types.organizations import OrganizationType, to_org_type


class OpenaiClients:
    def __init__(self, *args, **kwargs):
        self._oai_client: Optional["OpenAI"] = None
        self._aoai_client: Optional["AzureOpenAI"] = None
        self._ant_client: Optional["AnthropicOpenAI"] = None
        self._gg_client: Optional["GoogleOpenAI"] = None
        self._gq_client: Optional["GroqOpenAI"] = None
        self._pplx_client: Optional["PerplexityOpenAI"] = None
        self._vg_client: Optional["VoyageOpenAI"] = None
        self._models: List["Model"] = []

        _created = int(time.time())
        try:
            self._oai_client = OpenAI()
            self._models.extend(
                [
                    Model.model_validate(
                        {
                            "id": m,
                            "created": _created,
                            "object": "model",
                            "owned_by": OrganizationType.OPENAI.value,
                        }
                    )
                    for m in MODELS_OPENAI
                ]
            )
        except OpenAIError:
            languru_logger.warning("OpenAI client not initialized.")
        try:
            self._aoai_client = AzureOpenAI(api_version="2024-02-01")
            self._models.extend(
                [
                    Model.model_validate(
                        {
                            "id": m,
                            "created": _created,
                            "object": "model",
                            "owned_by": OrganizationType.AZURE.value,
                        }
                    )
                    for m in MODELS_AZURE_OPENAI
                ]
            )
        except OpenAIError:
            languru_logger.warning("Azure OpenAI client not initialized.")
        try:
            self._ant_client = AnthropicOpenAI()
            self._models.extend(
                [
                    Model.model_validate(
                        {
                            "id": m,
                            "created": _created,
                            "object": "model",
                            "owned_by": OrganizationType.ANTHROPIC.value,
                        }
                    )
                    for m in MODELS_ANTHROPIC
                ]
            )
        except CredentialsNotProvided:
            languru_logger.warning("Anthropic OpenAI client not initialized.")
        try:
            self._gg_client = GoogleOpenAI()
            self._models.extend(
                [
                    Model.model_validate(
                        {
                            "id": m,
                            "created": _created,
                            "object": "model",
                            "owned_by": OrganizationType.GOOGLE.value,
                        }
                    )
                    for m in MODELS_GOOGLE
                ]
            )
        except CredentialsNotProvided:
            languru_logger.warning("Google OpenAI client not initialized.")
        try:
            self._gq_client = GroqOpenAI()
            self._models.extend(
                [
                    Model.model_validate(
                        {
                            "id": m,
                            "created": _created,
                            "object": "model",
                            "owned_by": OrganizationType.GROQ.value,
                        }
                    )
                    for m in MODELS_GROQ
                ]
            )
        except CredentialsNotProvided:
            languru_logger.warning("Groq OpenAI client not initialized.")
        try:
            self._pplx_client = PerplexityOpenAI()
            self._models.extend(
                [
                    Model.model_validate(
                        {
                            "id": m,
                            "created": _created,
                            "object": "model",
                            "owned_by": OrganizationType.PERPLEXITY.value,
                        }
                    )
                    for m in MODELS_PERPLEXITY
                ]
            )
        except CredentialsNotProvided:
            languru_logger.warning("Perplexity OpenAI client not initialized.")
        try:
            self._vg_client = VoyageOpenAI()
            self._models.extend(
                [
                    Model.model_validate(
                        {
                            "id": m,
                            "created": _created,
                            "object": "model",
                            "owned_by": OrganizationType.VOYAGE.value,
                        }
                    )
                    for m in MODELS_VOYAGE
                ]
            )
        except CredentialsNotProvided:
            languru_logger.warning("Voyage OpenAI client not initialized.")

    def depends_org_type(
        self,
        request: Request,
        api_type: Optional[Text] = Query(None),
        org: Optional[Text] = Query(None),
        org_type: Optional[Text] = Query(None),
        organization: Optional[Text] = Query(None),
        organization_type: Optional[Text] = Query(None),
    ) -> Optional[OrganizationType]:
        """Returns the OpenAI client based on the request parameters."""

        logger = get_value_from_app(
            request.app, key="logger", value_typing=Logger, default=languru_logger
        )
        organization_type = (
            organization_type or organization or org_type or org or api_type
        )

        out: Optional[OrganizationType] = None
        if organization_type is not None:
            out = to_org_type(organization_type)
            logger.debug(f"Organization type: '{out}'.")
        return out

    def org_from_model(self, model: Text) -> Optional[OrganizationType]:
        """Returns the organization type based on the model name."""

        _model = (model.strip() if model else None) or None
        organization_type: Optional[OrganizationType] = None

        # Try to extract organization type from the model name
        if _model and "/" in _model:
            might_org = _model.split("/")[0]
            try:
                organization_type = to_org_type(might_org)
                languru_logger.debug(
                    f"Organization type: '{organization_type}' of '{_model}'."
                )
            except OrganizationNotFound:
                pass

        # Try search supported models
        if model is not None:
            for _c, _org in (
                (self._oai_client, OrganizationType.OPENAI),
                (self._aoai_client, OrganizationType.AZURE),
                (self._ant_client, OrganizationType.ANTHROPIC),
                (self._gg_client, OrganizationType.GOOGLE),
                (self._gq_client, OrganizationType.GROQ),
                (self._pplx_client, OrganizationType.PERPLEXITY),
                (self._vg_client, OrganizationType.VOYAGE),
            ):
                if _c is None:
                    continue
                if isinstance(_c, OpenAI):
                    if model in MODELS_OPENAI:
                        organization_type = _org
                        languru_logger.debug(
                            f"Organization type: '{organization_type}' of '{_model}'."
                        )
                        break
                elif isinstance(_c, AzureOpenAI):
                    if model in MODELS_AZURE_OPENAI:
                        organization_type = _org
                        languru_logger.debug(
                            f"Organization type: '{organization_type}' of '{_model}'."
                        )
                        break
                elif hasattr(_c, "models") and hasattr(_c.models, "supported_models"):
                    if model in _c.models.supported_models:  # type: ignore
                        organization_type = _org
                        languru_logger.debug(
                            f"Organization type: '{organization_type}' of '{_model}'."
                        )
                        break

        return organization_type

    def org_to_openai_client(
        self, org: Union[Text, "OrganizationType", Any]
    ) -> "OpenAI":
        """Returns the OpenAI client based on the organization type."""

        if not isinstance(org, OrganizationType):
            org = to_org_type(org)
        _client: Optional["OpenAI"] = None
        if org == OrganizationType.OPENAI:
            _client = self._oai_client
        elif org == OrganizationType.AZURE:
            _client = self._aoai_client
        elif org == OrganizationType.ANTHROPIC:
            _client = self._ant_client
        elif org == OrganizationType.GOOGLE:
            _client = self._gg_client
        elif org == OrganizationType.GROQ:
            _client = self._gq_client
        elif org == OrganizationType.PERPLEXITY:
            _client = self._pplx_client
        elif org == OrganizationType.VOYAGE:
            _client = self._vg_client
        else:
            raise OrganizationNotFound(f"Unknown organization: '{org}'.")
        if _client is None:
            raise OrganizationNotFound(
                f"Organization '{org}' client not not initialized."
            )
        return _client

    def models(self, model: Optional[Text] = None) -> List[Model]:
        """Returns the supported models based on the organization type."""

        if model is not None:
            for m in self._models:
                if m.id == model:
                    return [m.model_copy()]
            else:
                err_body = {
                    "error": {
                        "message": f"The model '{model}' does not exist",
                        "type": "invalid_request_error",
                        "param": "model",
                        "code": "model_not_found",
                    }
                }
                raise ModelNotFound(
                    f"Error code: {404} - {err_body}",
                )

        else:
            return [m.model_copy() for m in self._models]

    def default_openai_client(self) -> "OpenAI":
        """Returns the default OpenAI client."""

        # logger.warning("No organization type specified. Using OpenAI by default.")
        if self._oai_client is None:
            raise OrganizationNotFound("OpenAI client not initialized.")
        return self._oai_client


openai_clients = OpenaiClients()


# class Model(BaseModel):
#     id: str
#     """The model identifier, which can be referenced in the API endpoints."""

#     created: int
#     """The Unix timestamp (in seconds) when the model was created."""

#     object: Literal["model"]
#     """The object type, which is always "model"."""

#     owned_by: str
#     """The organization that owns the model."""
