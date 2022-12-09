import falcon
import jwt
from datetime import datetime, timedelta
import os

from src.data.db import Db


class Authenticate(object):

    def __int__(self):
        pass

    def encode(self, id_user):
        now = datetime.utcnow()
        payload = {
            'id': id_user,
            'iat': now,
            'exp': (now + timedelta(hours=24)).timestamp()
        }

        token = jwt.encode(
            payload=payload,
            key=os.getenv("JWT_SECRET"),
            algorithm="HS256"
        )

        return token

    def decode_and_validate_token(self, access_token):
        unverified_headers = jwt.get_unverified_header(access_token)
        return jwt.decode(
            access_token,
            key=os.getenv("JWT_SECRET"),
            algorithms=unverified_headers['alg']
        )

    def __auth_basic(self, username, password):
        if True:
            print("You have access")
        else:
            raise falcon.HTTPUnauthorized('Unauthorized', 'You have no access')

    def __call__(self, req, resp, resource, params, role):

        print("Before trigger - class: Authorize")

        token = req.get_header('Authorization')

        # IL FAUT QUE JE METTE LE SERVICE EN SINGLETON POUR AUTH ou que j'utilise la db pour recup l'user

        try:
            decodedToken = self.decode_and_validate_token(token)
        except jwt.exceptions.DecodeError as err:
            raise falcon.HTTPUnauthorized('Unauthorized', 'Token expired')

        db = Db.getInstance()
        cur = db.conn.cursor()

        cur.execute("SELECT * FROM youshare.users WHERE id_user=%s", [decodedToken['id']])
        data = cur.fetchone()

        db.conn.commit()
        cur.close()

        if data[2] != role:
            db.conn.commit()
            cur.close()
            raise falcon.HTTPUnauthorized('Unauthorized','You don\'t have the right to access this data')

        req.context.user = {
            "id":data[0],
            "username":data[1],
            "role":data[2],
            "email":data[3]
        }

        if token:
            pass
        else:
            raise falcon.HTTPNotImplemented('Not Implemented', 'Please specify a token')
