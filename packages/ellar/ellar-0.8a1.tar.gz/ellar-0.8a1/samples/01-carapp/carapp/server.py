import os

from ellar.app import AppFactory
from ellar.common.constants import ELLAR_CONFIG_MODULE
from ellar.core import LazyModuleImport as lazyLoad
from ellar.openapi import (
    OpenAPIDocumentBuilder,
    OpenAPIDocumentModule,
    ReDocUI,
    SwaggerUI,
)

application = AppFactory.create_from_app_module(
    lazyLoad("carapp.root_module:ApplicationModule"),
    config_module=os.environ.get(
        ELLAR_CONFIG_MODULE, "carapp.config:DevelopmentConfig"
    ),
)

document_builder = OpenAPIDocumentBuilder()
document_builder.set_title("Ellar API").set_version("1.0.2").set_contact(
    name="John Doe", url="https://www.yahoo.com", email="johnDoe@gmail.com"
).set_license("MIT Licence", url="https://www.google.com")

document = document_builder.build_document(application)
OpenAPIDocumentModule.setup(
    app=application,
    docs_ui=[ReDocUI(), SwaggerUI()],
    document=document,
    guards=[],
)
