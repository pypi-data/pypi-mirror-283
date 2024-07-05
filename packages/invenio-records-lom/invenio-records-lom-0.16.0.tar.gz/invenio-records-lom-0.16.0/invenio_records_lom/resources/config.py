# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REST API configuration."""

import marshmallow
from flask_resources import JSONSerializer, ResponseHandler
from invenio_rdm_records.resources import IIIFResourceConfig
from invenio_records_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.files import FileResourceConfig

from .serializers import LOMToUIJSONSerializer

record_serializer = {
    "application/json": ResponseHandler(JSONSerializer()),
    "application/vnd.inveniolom.v1+json": ResponseHandler(LOMToUIJSONSerializer()),
}

url_prefix = "/oer"


class LOMDraftFilesResourceConfig(FileResourceConfig):
    """LOM Draft Files Resource configuration."""

    blueprint_name = "lom_draft_files"
    url_prefix = f"{url_prefix}/<pid_value>/draft"


class LOMRecordFilesResourceConfig(FileResourceConfig):
    """LOM Record Files Resource configuration."""

    allow_upload = False
    blueprint_name = "lom_record_files"
    url_prefix = f"{url_prefix}/<pid_value>"


class LOMRecordResourceConfig(RecordResourceConfig):
    """LOM Record Resource configuration."""

    blueprint_name = "lom_records"
    url_prefix = url_prefix

    default_accept_mimetype = "application/json"

    routes = {
        "list": "",
        "item": "/<pid_value>",
        "item-draft": "/<pid_value>/draft",
        "item-publish": "/<pid_value>/draft/actions/publish",
        "item-pids-reserve": "/<pid_value>/draft/pids/<scheme>",
        "user-prefix": "/user",
    }

    request_view_args = {
        "pid_value": marshmallow.fields.Str(),
        "scheme": marshmallow.fields.Str(),
    }

    response_handlers = record_serializer


class LOMIIIFResourceConfig(IIIFResourceConfig):
    """LOM IIIF Resource Config."""

    blueprint_name = "lom_iiif"
    url_prefix = f"{url_prefix}/iiif"
