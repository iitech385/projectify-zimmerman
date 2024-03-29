from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from zimmerman.main import limiter
from ..util.dto import UserDto
from ..service.user_service import UserService, load_user

api = UserDto.api
_user = UserDto.user
_user_update = UserDto.user_update


@api.route("/get/<string:username>")
class UserGet(Resource):
    @api.doc(
        "Get a specific user",
        responses={200: "User data has been sent", 404: "User not found!"},
    )
    @jwt_required
    def get(self, username):
        """ Get a specific user by their username """
        return UserService.get_user_info(username)


@api.route("/update")
class UserUpdate(Resource):
    @api.expect(_user_update)
    @api.doc(
        "Update a user' information",
        responses={200: "User data has been updated.", 404: "User not found!"},
    )
    @jwt_required
    def put(self):
        """ Update a user's data """
        current_user = load_user(get_jwt_identity())
        data = request.get_json()

        return UserService.update(data, current_user)
