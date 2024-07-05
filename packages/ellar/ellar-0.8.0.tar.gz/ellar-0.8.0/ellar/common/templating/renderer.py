import typing as t
from functools import lru_cache

import jinja2
from ellar.common.templating import Environment
from starlette.background import BackgroundTask
from starlette.templating import _TemplateResponse as TemplateResponse

if t.TYPE_CHECKING:  # pragma: no cover
    from ellar.core.connection import Request


@lru_cache(1200)
def get_template_name(template_name: str) -> str:
    if not template_name.endswith(".html"):
        return template_name + ".html"
    return template_name


def process_view_model(view_response: t.Any) -> t.Dict:
    if isinstance(view_response, dict):
        return view_response
    return {"model": view_response}


def _get_jinja_and_template_context(
    template_name: str, request: "Request", **context: t.Any
) -> t.Tuple["jinja2.Template", t.Dict]:
    jinja_environment = request.service_provider.get(Environment)
    jinja_template = jinja_environment.get_template(get_template_name(template_name))
    template_context = dict(context)
    template_context.update(request=request)
    return jinja_template, template_context


def render_template_string(
    template_string: str, request: "Request", **template_context: t.Any
) -> str:
    """Renders a template to string.
    :param request: Request instance
    :param template_string: Template String
    :param template_context: variables that should be available in the context of the template.
    """
    try:
        jinja_template, template_context_ = _get_jinja_and_template_context(
            template_name=template_string,
            request=request,
            **process_view_model(template_context),
        )
        return jinja_template.render(template_context_)
    except jinja2.TemplateNotFound:
        jinja_environment = request.service_provider.get(Environment)
        jinja_template = jinja_environment.from_string(template_string)

        _template_context = dict(template_context)
        _template_context.update(request=request)

        return jinja_template.render(_template_context)


def render_template(
    template_name: str,
    request: "Request",
    background: t.Optional[BackgroundTask] = None,
    status_code: int = 200,
    **template_kwargs: t.Any,
) -> TemplateResponse:
    """Renders a template from the template folder with the given context.
    :param status_code: Template Response status code
    :param request: Request instance
    :param template_name: the name of the template to be rendered
    :param template_kwargs: variables that should be available in the context of the template.
    :param background: any background task to be executed after render.
    :return TemplateResponse
    """
    jinja_template, template_context = _get_jinja_and_template_context(
        template_name=template_name,
        request=request,
        **process_view_model(template_kwargs),
    )
    return TemplateResponse(
        template=jinja_template,
        context=template_context,
        background=background,
        status_code=status_code,
    )
