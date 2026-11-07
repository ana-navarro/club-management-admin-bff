from dataclasses import dataclass

from src.domain.ports.auth_ports import (
    ClientInfo,
    ForgotPasswordPort,
    GetCurrentUserPort,
    JsonObject,
    LoginPort,
    RefreshTokenPort,
    ResetPasswordPort,
    UpdatePreferencesPort,
    UpstreamError,
)

ADMIN_USER_TYPE = "ADMIN"


@dataclass(frozen=True)
class AuthUsecases:
    login_user: LoginPort
    refresh_token: RefreshTokenPort
    forgot_password: ForgotPasswordPort
    reset_password: ResetPasswordPort
    get_current_user: GetCurrentUserPort
    update_preferences: UpdatePreferencesPort

    def login(
        self, email: str, password: str, preferences: JsonObject, client: ClientInfo
    ) -> JsonObject:
        """Logs in as an administrator and saves the session choices the user does not have."""
        body: JsonObject = {"email": email, "password": password, "userType": ADMIN_USER_TYPE}
        if client.ip:
            body["ip"] = client.ip
        if client.user_agent:
            body["userAgent"] = client.user_agent
        if preferences.get("language"):
            body["language"] = preferences["language"]

        session = self.login_user(body)

        saved = session["user"]["preferences"]
        missing = {
            name: value
            for name, value in preferences.items()
            if value is not None and saved.get(name) is None
        }
        if not missing:
            return session

        try:
            session["user"] = self.update_preferences(f"Bearer {session['token']}", missing)
        except UpstreamError:
            # The login is valid. Failing to save a preference must not block it.
            pass
        return session
