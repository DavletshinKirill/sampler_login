# from .model import Users, Permissions
# from sqlalchemy import event
# from flask import request
#
# permissions_dictionary = {
#     "ADMIN": [Permissions.ADMIN],
#     "MODERATE": [Permissions.MODERATE, Permissions.ADMIN],
#     "WRITE": [Permissions.MODERATE, Permissions.ADMIN, Permissions.WRITE],
#     "COMMENT": [Permissions.MODERATE, Permissions.ADMIN, Permissions.WRITE, Permissions.COMMENT],
#     "FOLLOW": [Permissions.MODERATE, Permissions.ADMIN, Permissions.WRITE, Permissions.COMMENT, Permissions.FOLLOW]
# }
#
#
# @event.listens_for(Users, "load")
# def add_user(*args, **kwargs):
#     user = Users.query.get(request.args.get('user_id'))
#     print(user)
#     print('function is called')
#     #if permissions_dictionary["ADMIN"]