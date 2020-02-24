from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql

# 建立白名單
parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("gender")
parser.add_argument("birth")
parser.add_argument("note")


class Users(Resource):

    def db_init(self):
        db = pymysql.connect('127.0.0.1', 'root', 'root', 'flask')
        cursor = db.cursor(pymysql.cursors.DictCursor)  # 若無Dict，則預設會是tuple
        return db, cursor

    def get(self):
        db, cursor = self.db_init()

        sql = """
            select * from flask.users where deleted != True 
        """

        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()

        response = {}
        response['code'] = 200
        response['msg'] = 'success'
        response['data'] = users

        return jsonify(response)

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        response = {}

        if arg["name"] == None:  # 必須要給 name值，否則會跳錯
            response['code'] = 400
            response['msg'] = "name undetected"
            return jsonify(response)

        user = {
            "name": arg["name"],
            "gender": arg["gender"],
            "birth": arg["birth"] or "1900-01-01",
            "note": arg["note"]
        }
        sql = """
            Insert into flask.users(name,gender,birth,note)
            Values('{}','{}','{}','{}')
        """.format(user["name"], user["gender"], user["birth"], user["note"])
        result = cursor.execute(sql)
        db.commit()
        db.close()

        response = {}
        if result == 0:
            response['code'] = 500
            response['msg'] = 'error'
        else:
            response['code'] = 200
            response['msg'] = 'success'

        return jsonify(response)


class User(Resource):
    def db_init(self):
        db = pymysql.connect('127.0.0.1', 'root', 'root', 'flask')
        cursor = db.cursor(pymysql.cursors.DictCursor)  # 若無Dict，則預設會是tuple
        return db, cursor

    def get(self, id):  # search one ID
        db, cursor = self.db_init()

        sql = """
            select * from flask.users where id = '{}' and deleted != True
        """.format(id)

        cursor.execute(sql)
        users = cursor.fetchone()  # 若此還是用fetchall的話會回傳一個陣列
        db.close()

        response = {}
        response['code'] = 200
        response['msg'] = 'success'
        response['data'] = users

        return jsonify(response)

    def put(self, id):  # update one ID's all keys
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            "name": arg["name"],
            "gender": arg["gender"],
            "birth": arg["birth"] or "1900-01-01",
            "note": arg["note"]
        }

        sql = """
            Update flask.users
            Set name = "{}" , gender = "{}" , birth = "{}" , note = "{}"
            Where id = {} and deleted != True
        """.format(user["name"], user["gender"], user["birth"], user["note"], id)

        result = cursor.execute(sql)
        db.commit()
        db.close()

        response = {}
        if result == 0:
            response['code'] = 500
            response['msg'] = 'error'
        else:
            response['code'] = 200
            response['msg'] = 'success'

        return jsonify(response)

    def patch(self, id):  # update one ID's one(or more) key
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            "name": arg["name"],
            "gender": arg["gender"],
            "birth": arg["birth"],
            "note": arg["note"]
        }

        query = []
        for key, value in user.items():
            if value != None:
                query.append(key + " = '{}' ".format(value))

        query = ",".join(query)

        sql = """
            Update flask.users
            Set {}
            Where id = '{}' and deleted != True
        """.format(query, id)

        result = cursor.execute(sql)
        db.commit()
        db.close()

        response = {}
        if result == 0:
            response['code'] = 500
            response['msg'] = 'error'
        else:
            response['code'] = 200
            response['msg'] = 'success'

        return jsonify(response)

    # def delete(self, id):  # HARD delete one ID's all keys
    #     db, cursor = self.db_init()

    #     sql = """
    #         Delete from flask.users
    #         Where id = '{}'
    #     """.format(id)

    #     result = cursor.execute(sql)
    #     db.commit()
    #     db.close()

    #     response = {}
    #     if result == 0:
    #         response['code'] = 500
    #         response['msg'] = 'error'
    #     else:
    #         response['code'] = 200
    #         response['msg'] = 'success'

    #     return jsonify(response)

    def delete(self, id):  # SOFT delete one ID's all keys
        db, cursor = self.db_init()

        sql = """
            Update flask.users
            Set deleted = True
            Where id = '{}' and deleted != True
        """.format(id)

        result = cursor.execute(sql)
        db.commit()
        db.close()

        response = {}
        if result == 0:
            response['code'] = 500
            response['msg'] = 'error'
        else:
            response['code'] = 200
            response['msg'] = 'success'

        return jsonify(response)
