from attr import dataclass


@dataclass
class RefreshTokenRequest:
    token : str