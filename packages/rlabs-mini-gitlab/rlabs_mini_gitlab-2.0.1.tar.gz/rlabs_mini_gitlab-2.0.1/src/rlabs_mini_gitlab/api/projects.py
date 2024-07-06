#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini Gitlab.
#
# RLabs Mini Gitlab is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini Gitlab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini Gitlab. If not, see <http://www.gnu.org/licenses/>.
#
'''
    Projects API

    /projects

    https://docs.gitlab.com/ee/api/projects.html
'''
import logging
from logging import getLogger
from typing import ClassVar
from typing import Any
from rlabs_mini_api.request import GET
from rlabs_mini_box.data import Box
from typing import Optional
from rlabs_mini_cache.cache import Cache

from rlabs_mini_gitlab import api_kwargs
from rlabs_mini_gitlab import config as global_config
from rlabs_mini_gitlab import common

class Projects:
    '''
        Projects
    '''
    logger: ClassVar[logging.Logger] = getLogger("dummy")   # dummy logger to avoid type errors
                                                            # will never be used
    mini_cache: ClassVar[Optional[Cache]] = None
    _configured: ClassVar[bool] = False

    @classmethod
    def config(
        cls,
        logger: logging.Logger,
        mini_cache: Optional[Cache] = None
    ) -> None:
        '''
            config

            Configures the class logger
        '''
        cls.logger = logger
        cls.mini_cache = mini_cache
        cls._configured = True

    @classmethod
    def details(
            cls,
            project_id: int,
            **kwargs: Any,
        ) -> Box:
        '''
            Details

            GET /projects/:id
        '''
        common.api_entry_protocol(
            cls,
            kwargs,
            f"Getting details for project with ID: {project_id}"
        )

        request = (
            GET
                .projects
                .id(project_id, **kwargs)
        )

        python_data = common.exec_cached_request(
            request,
            cls.mini_cache
        )

        return Box(python_data)

    @classmethod
    def projects(
            cls,
            per_page: int = global_config.per_page_default,
            **kwargs: Any,
        ) -> Box:
        '''
            Projects

            GET /projects
        '''
        common.api_entry_protocol(
            cls,
            kwargs,
            "Getting projects"
        )

        collected: list = []
        page = 1

        while True:

            kwargs.update({
                "per_page": per_page,
                "page": page
            })

            request = (
                GET
                    .projects(**kwargs)
            )

            python_data = common.exec_cached_request(
                request,
                cls.mini_cache
            )

            if not python_data:
                break

            collected += python_data
            page += 1

        return Box(collected)

    @classmethod
    def variables(
            cls,
            project_id: int,
            per_page: int = global_config.per_page_default,
            **kwargs: Any,
        ) -> Box:
        '''
            Variables

            GET /projects/:id/variables
        '''
        common.api_entry_protocol(
            cls,
            kwargs,
            f"Getting variables for project with ID: {project_id}"
        )

        collected: list = []
        page = 1

        while True:

            kwargs.update({
                "per_page": per_page,
                "page": page
            })

            request = (
                GET
                    .projects
                    .id(project_id)
                    .variables(**kwargs)
            )

            python_data = common.exec_cached_request(
                request,
                cls.mini_cache
            )

            if not python_data:
                break

            collected += python_data
            page += 1

        return Box(collected)
