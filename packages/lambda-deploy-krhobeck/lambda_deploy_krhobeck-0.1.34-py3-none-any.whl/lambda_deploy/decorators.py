from functools import wraps
from typing import Dict, Any, Optional, Callable

from lambda_deploy.pydantic_models import CorsConfig, IAMConfig

lambda_functions = []


def lambda_function(
    name: str,
    handler: str,
    file_path: str,
    s3_bucket: str,
    s3_key: str,
    role_name: str,
    runtime: str = "python3.10",
    http_method: Optional[str] = None,
    endpoint: Optional[str] = None,
    cors_config: Optional[Dict[str, Any]] = None,
    iam_config: Optional[Dict[str, Any]] = None,
):
    if cors_config:
        cors_config = CorsConfig(**cors_config)
    if iam_config:
        iam_config = IAMConfig(**iam_config)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper._lambda_meta = {
            "name": name,
            "runtime": runtime,
            "handler": handler,
            "file_path": file_path,
            "s3_bucket": s3_bucket,
            "s3_key": s3_key,
            "role_name": role_name if role_name else None,
            "http_method": http_method,
            "endpoint": endpoint,
            "cors_config": cors_config if cors_config else None,
            "iam_config": iam_config if iam_config else None,
        }
        lambda_functions.append(wrapper)
        return wrapper

    return decorator
