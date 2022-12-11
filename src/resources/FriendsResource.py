import falcon
from json import dumps
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.services.FriendsService import FriendsService
from src.utils import enum

auth = Authenticate()


class Friends:
    def __init__(self):
        self.friendsService = FriendsService.getInstance()

    @falcon.before(auth, enum.ROLE_USER)
    def on_get(self, req, resp):
        list_friends = self.friendsService.getAll(req.context.user['id_user'])

        resp.status = falcon.HTTP_200
        resp.body = dumps(list_friends)

    @falcon.before(auth,enum.ROLE_USER)
    def on_get_requests(self,req,resp):
        pass

    @falcon.before(auth, enum.ROLE_USER)
    def on_get_self(self,req,resp):
        pass

    @falcon.before(auth,enum.ROLE_USER)
    def on_post_id(self,req,resp,id_friend):
        self.friendsService.addFriendRequest(req.context.user['id_user'],int(id_friend))
        resp.status = falcon.HTTP_201


    @falcon.before(auth,enum.ROLE_USER)
    def on_delete_id(self,req,resp,id_friend):
        self.friendsService.deleteFriendRequest(req.context.user['id_user'], int(id_friend))
        resp.status = falcon.HTTP_200

    @falcon.before(auth,enum.ROLE_USER)
    def on_post_accept(self,req,resp,id_friend):

        self.friendsService.acceptFriendRequest(req.context.user['id_user'], int(id_friend))
        resp.status = falcon.HTTP_200

    @falcon.before(auth,enum.ROLE_USER)
    def on_post_refuse(self,req,resp,id_friend):
        pass


