from typing import List

import psycopg2
import sqlalchemy

from dao.environment_dao import EnvironmentDAO
from exception.environment_exception import EnvironmentException
from model.environment import Environment
from util.logging import logger


class EnvironmentService:
    def __init__(self, environment_dao: EnvironmentDAO):
        self._environment_dao = environment_dao

    def create(self, name: str, docker_image: str) -> Environment:
        logger.info("Creating a new environment: name=%s, docker_image=%s", name, docker_image)

        if not name or not docker_image:
            raise EnvironmentException('Name and Docker image are required.', 400)

        environment = Environment(name, docker_image)
        try:
            environment = self._environment_dao.insert(environment)
            logger.info("Created environment %s", environment)
            return environment
        except Exception as e:
            logger.error("Could not create the new environment due to %s", e)
            if isinstance(e, psycopg2.errors.UniqueViolation) or isinstance(e, sqlalchemy.exc.IntegrityError):
                raise EnvironmentException("Environment parameters {name, docker_image} must be unique.", 409)
            raise EnvironmentException("Environment creation failed.", 500)

    def list_environments(self) -> List[Environment]:
        logger.info("List all environments...")
        return self._environment_dao.find_all()

    def get_environment(self, environment_id) -> Environment:
        logger.info(f"Get the environment: {environment_id}")
        environment = self._environment_dao.find_by_id(environment_id)

        if environment is None:
            raise EnvironmentException(f"Environment[id = {environment_id}] not found.", 404)

        return environment

    def update_environment(self, environment_id: str, name: str, docker_image: str) -> Environment:
        logger.info(f"Update the environment: {environment_id} with name = {name}, docker_image = {docker_image}")

        if not name or not docker_image:
            raise EnvironmentException('Name and Docker image are required.', 400)

        environment = self.get_environment(environment_id)

        environment.name = name
        environment.docker_image = docker_image

        try:
            self._environment_dao.session_commit()
            return environment
        except Exception as e:
            logger.error("Could not update the existing environment due to %s", e)
            if isinstance(e, psycopg2.errors.UniqueViolation) or isinstance(e, sqlalchemy.exc.IntegrityError):
                raise EnvironmentException("Environment parameters {name, docker_image} must be unique.", 409)
            raise EnvironmentException("Environment update failed.", 500)

    def delete_environment(self, environment_id) -> None:
        logger.info(f"Delete the environment: {environment_id}")
        return self._environment_dao.delete_by_id(environment_id)
