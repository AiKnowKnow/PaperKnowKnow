from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw.strip())
    except Exception:
        return default


def _env_list(name: str, default: list[str]) -> list[str]:
    raw = os.getenv(name)
    if not raw:
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


@dataclass(frozen=True)
class AppSettings:
    app_name: str
    env: str
    desktop_mode: bool
    host: str
    port: int
    open_browser: bool
    max_upload_size_mb: int
    rate_limit_calls: int
    rate_limit_window_sec: int
    cors_origins: list[str]
    trusted_hosts: list[str]
    data_dir_override: str


def load_settings() -> AppSettings:
    env = os.getenv("PAPER_ENV", "development").strip().lower()
    desktop_mode = _env_bool("PAPER_DESKTOP_MODE", default=False)
    default_host = "127.0.0.1" if desktop_mode or env == "development" else "0.0.0.0"
    default_open_browser = desktop_mode or env == "development"

    return AppSettings(
        app_name=os.getenv("PAPER_APP_NAME", "PaperKnowKnow").strip() or "PaperKnowKnow",
        env=env,
        desktop_mode=desktop_mode,
        host=os.getenv("PAPER_HOST", default_host).strip() or default_host,
        port=_env_int("PAPER_PORT", 8000),
        open_browser=_env_bool("PAPER_OPEN_BROWSER", default=default_open_browser),
        max_upload_size_mb=_env_int("PAPER_MAX_UPLOAD_MB", 50),
        rate_limit_calls=_env_int("PAPER_RATE_LIMIT_CALLS", 30),
        rate_limit_window_sec=_env_int("PAPER_RATE_LIMIT_WINDOW_SEC", 60),
        cors_origins=_env_list(
            "PAPER_CORS_ORIGINS",
            ["http://127.0.0.1:8000", "http://localhost:8000"] if env == "development" else [],
        ),
        trusted_hosts=_env_list(
            "PAPER_TRUSTED_HOSTS",
            ["127.0.0.1", "localhost"] if env == "development" else ["*"],
        ),
        data_dir_override=os.getenv("PAPER_DATA_DIR", "").strip(),
    )


def resolve_data_dir(settings: AppSettings, *, frozen: bool, platform: str, cwd: Path, home: Path) -> Path:
    if settings.data_dir_override:
        p = Path(settings.data_dir_override).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p

    if frozen:
        if platform == "darwin":
            base = home / "Library" / "Application Support" / settings.app_name
        elif platform == "win32":
            base = Path(os.environ.get("APPDATA", home)) / settings.app_name
        else:
            base = home / f".{settings.app_name.lower()}"
        try:
            base.mkdir(parents=True, exist_ok=True)
            return base
        except OSError:
            fallback = home / "Documents" / settings.app_name
            try:
                fallback.mkdir(parents=True, exist_ok=True)
                return fallback
            except OSError:
                local = cwd / f"{settings.app_name}Data"
                local.mkdir(parents=True, exist_ok=True)
                return local

    if settings.env == "production":
        base = home / f".{settings.app_name.lower()}"
        base.mkdir(parents=True, exist_ok=True)
        return base

    return cwd
