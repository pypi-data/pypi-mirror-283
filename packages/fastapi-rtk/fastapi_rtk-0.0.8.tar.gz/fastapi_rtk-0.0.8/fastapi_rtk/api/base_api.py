from typing import Any, Dict

from fastapi import APIRouter, Depends

from ..const import PERMISSION_PREFIX
from ..utils import update_self_signature


class BaseApi:
    """
    Base Class for FastAPI APIs.
    """

    version = "v1"
    """
    Version for the API. Defaults to "v1".
    """
    resource_name: str = None
    """
    The name of the resource. If not given, will use the class name.
    """
    base_permissions: list[str] | None = None
    """
    List of base permissions for the API. Defaults to None.

    Example:
        base_permissions = ["can_get", "can_post"]
    """
    router: APIRouter = None
    """
    The FastAPI router object.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    permissions: list[str] = None
    """
    List of permissions for the API.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    toolkit = None
    """
    The FastapiReactToolkit object. Automatically set when the API is added to the toolkit.
    """
    _cache: Dict[str, Any] = None
    """
    The cache for the API.
    
    DO NOT MODIFY.
    """

    def __init__(self):
        self.resource_name = self.resource_name or self.__class__.__name__.lower()
        self.router = self.router or APIRouter(
            prefix=f"/api/{self.version}/{self.resource_name}",
            tags=[self.__class__.__name__],
        )
        self.permissions = self.permissions or []

    def integrate_router(self, app: APIRouter):
        """
        Integrate the router into the toolkit.

        This will manage all decorators like @expose, @permission_name, etc.

        DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
        """
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, "_permission_name"):
                self.permissions.append(f"{PERMISSION_PREFIX}{attr._permission_name}")
            if hasattr(attr, "_urls"):
                for data in attr._urls:
                    if hasattr(attr, "_response_model_str"):
                        data["response_model"] = getattr(self, attr._response_model_str)

                    extra_dependencies = []
                    if hasattr(attr, "_dependencies"):
                        extra_dependencies = attr._dependencies
                    if extra_dependencies and not data.get("dependencies"):
                        data["dependencies"] = []
                    for dep in extra_dependencies:
                        func, kwargs = dep
                        if kwargs:
                            for key, val in kwargs.items():
                                if val == ":self":
                                    kwargs[key] = self
                            func = Depends(func(**kwargs))
                        else:
                            func = Depends(func)
                        data["dependencies"].append(func)

                    methods = data["methods"]
                    data.pop("methods")

                    for method in methods:
                        method = method.lower()
                        router_func = getattr(self.router, method)

                        # If it is a bound method of a class, get the function
                        if hasattr(attr, "__func__"):
                            attr = attr.__func__

                        #! Update self parameter in the function signature, so that self is not treated as a parameter
                        update_self_signature(self, attr)

                        # Add the route to the router
                        router_func(**data)(attr)

        if getattr(self, "_init_routes", None):
            self._init_routes()
        app.include_router(self.router)

    @property
    def cache(self):
        """
        Returns the cache dictionary.

        If the cache dictionary is not initialized, it initializes it as an empty dictionary.

        Returns:
            dict: The cache dictionary.
        """
        if not self._cache:
            self._cache = {}
        return self._cache
