from flask import request

from app import db, session, app
from dao.environment_dao import EnvironmentDAO
from exception.environment_exception import EnvironmentException
from service.environment_service import EnvironmentService
from util.logging import logger
from json import loads

SESSION_HEADER_KEY = 'x-dali-session'

# instances
environment_dao = EnvironmentDAO(session)
environment_service = EnvironmentService(environment_dao)

@app.route('/api/v1/environments', methods=['POST'])
def create_environment():
    payload = loads(request.data)
    logger.info("Received a request to create an environment: %s", payload)

    name = payload.get('name')
    docker_image = payload.get('docker_image')

    enviroment = environment_service.create(name, docker_image)
    return enviroment.to_dict(), 201


@app.route('/api/v1/environments', methods=['GET'])
def list_environments():
    logger.info("Received a request to list all environments")
    return {'environments': [environment.to_dict() for environment in environment_service.list_environments()]}, 200


@app.route('/api/v1/environments/<environment_id>', methods=['GET', 'DELETE', 'PUT'])
def single_environment_actions(environment_id):
    # _check_session(request)
    if request.method == 'GET':
        logger.info("Received a request to get the environment")
        return environment_service.get_environment(environment_id).to_dict(), 200

    elif request.method == 'DELETE':
        logger.info("Received a request to delete the environment")
        environment_service.delete_environment(environment_id)
        return "", 204

    elif request.method == 'PUT':
        payload = loads(request.data)
        logger.info("Received a request to update an environment: %s", payload)

        name = payload.get('name')
        docker_image = payload.get('docker_image')

        logger.info("Received a request to update the environment")
        return environment_service.update_environment(environment_id, name, docker_image).to_dict(), 200

    return {'error': 'Internal Server Error'}, 500


@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f'An error occurred: {error}')
    if isinstance(error, EnvironmentException):
        return {'error': error.message}, error.status

    return {'error': 'Internal Server Error'}, 500


if __name__ == "__main__":
    with app.app_context() as context:
        db.create_all()
    app.run()
