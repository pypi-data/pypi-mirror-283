##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import base


class Main(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.strongRef`."""

    cid: str  #: Cid.
    uri: str  #: Uri.

    py_type: t.Literal['com.atproto.repo.strongRef'] = Field(
        default='com.atproto.repo.strongRef', alias='$type', frozen=True
    )
