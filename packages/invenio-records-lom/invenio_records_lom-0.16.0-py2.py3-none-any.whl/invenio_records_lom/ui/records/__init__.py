# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2021 CERN.
# Copyright (C) 2019-2021 Northwestern University.
# Copyright (C)      2021 TU Wien.
# Copyright (C) 2021-2023 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""User interface utilities for records."""

from flask import Blueprint, Flask
from flask_menu import current_menu
from invenio_i18n import lazy_gettext as _
from invenio_pidstore.errors import (
    PIDDeletedError,
    PIDDoesNotExistError,
    PIDUnregistered,
)
from invenio_records_resources.services.errors import PermissionDeniedError

from .deposits import deposit_create, deposit_edit, uploads
from .errors import (
    not_found_error,
    record_permission_denied_error,
    record_tombstone_error,
)
from .records import (
    record_detail,
    record_export,
    record_file_download,
    record_file_preview,
    record_from_pid,
    record_latest,
)


def init_records_views(blueprint: Blueprint, app: Flask):
    """Register blueprints for records on passed in `blueprint`."""
    routes = app.config["LOM_ROUTES"]
    app_ext = app.extensions["invenio-records-lom"]
    with app.app_context():
        schemes = app_ext.records_service.config.pids_providers

    blueprint.add_url_rule(
        routes["uploads"],
        view_func=uploads,
    )
    blueprint.add_url_rule(
        routes["deposit_create"],
        view_func=deposit_create,
    )
    blueprint.add_url_rule(
        routes["deposit_edit"],
        view_func=deposit_edit,
    )
    blueprint.add_url_rule(
        routes["record_detail"],
        view_func=record_detail,
    )
    blueprint.add_url_rule(
        routes["record_export"],
        view_func=record_export,
    )
    blueprint.add_url_rule(
        routes["record_file_preview"],
        view_func=record_file_preview,
    )
    blueprint.add_url_rule(
        routes["record_file_download"],
        view_func=record_file_download,
    )
    blueprint.add_url_rule(
        routes["record_latest"],
        view_func=record_latest,
    )
    if schemes:
        blueprint.add_url_rule(
            routes["record_from_pid"].format(schemes=",".join(schemes)),
            view_func=record_from_pid,
        )

    # Register error handlers
    blueprint.register_error_handler(PIDDeletedError, record_tombstone_error)
    blueprint.register_error_handler(PIDDoesNotExistError, not_found_error)
    blueprint.register_error_handler(PIDUnregistered, not_found_error)
    blueprint.register_error_handler(KeyError, not_found_error)
    blueprint.register_error_handler(
        PermissionDeniedError, record_permission_denied_error
    )

    # register dashboard-tab
    @blueprint.before_app_first_request
    def register_lom_dashboard_tab():
        """Register entry for lom in the `flask_menu`-submenu "dashboard"."""
        user_dashboard_menu = current_menu.submenu("dashboard")
        user_dashboard_menu.submenu("OER").register(
            "invenio_records_lom.uploads",  # <blueprint-name>.<view-func-name>
            text=_("Educational Resources"),
            order=5,
            # visible_when=...,
            # :callable[[], bool], flask_login.current_user.is_authenticated and Permission(<perm>).can()
            # perm = flask_principal.<SomeKindOfNeed>("name-of-need")
        )
