from flask_restful import Resource, reqparse
from models.users import UserModel

# Variable that will allow us to parse the data
_user_parser = reqparse.RequestParser()
# Here is where we specify the fields that we want from the payload
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help='This field cannot be left blank!')
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='This field cannot be left blank!')


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if(UserModel.find_by_email(data['email'])):
            return {'message': 'Email already used!'}

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created succesfully!'}, 201

