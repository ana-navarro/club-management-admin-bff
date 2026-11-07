from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Theme = Literal["light", "dark"]
Language = Literal["pt-BR", "en"]


class PreferencesDto(BaseModel):
    theme: Theme | None = None
    language: Language | None = None


class LoginRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)
    preferences: PreferencesDto = PreferencesDto()


class ForgotPasswordRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=3, max_length=254)
    language: Language | None = None


class ResetPasswordRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    token: str = Field(min_length=1, max_length=256)
    password: str = Field(min_length=1, max_length=256)


class UpdatePreferencesRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    theme: Theme | None = None
    language: Language | None = None


class ClubDto(BaseModel):
    id: str
    name: str


class UserDto(BaseModel):
    """The user sent to the frontend. Any other field from the service is dropped."""

    id: str
    name: str
    email: str
    type: Literal["ADMIN", "CLIENT"]
    clubs: list[ClubDto]
    preferences: PreferencesDto


class SessionDto(BaseModel):
    token: str
    expiresAt: str  # noqa: N815
    renewAt: str  # noqa: N815


class LoginResponseDto(SessionDto):
    user: UserDto
