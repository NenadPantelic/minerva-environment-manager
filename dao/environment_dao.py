from exception.environment_exception import EnvironmentException
from model.environment import Environment


class EnvironmentDAO:
    def __init__(self, session):
        self._session = session

    def session_commit(self):
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    def insert(self, environment: Environment):
        try:
            self._session.add(environment)
            self._session.commit()
            return environment
        except Exception as e:
            self._session.rollback()
            raise e

    def find_all(self):
        return Environment.query.all()

    def find_by_id(self, id):
        return Environment.query.get(id)

    def delete_by_id(self, id):
        try:
            environment = self.find_by_id(id)
            if environment is None:
                raise EnvironmentException(f'The environment with id {id} not found', 404)

            self._session.delete(environment)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
