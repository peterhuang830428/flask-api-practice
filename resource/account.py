from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql

parser = reqparse.RequestParser()
parser.add_argument("balance")
parser.add_argument("account_number")
parser.add_argument("user_id")


class Accounts(Resource):

    def db_init(self):
        db = pymysql.connect('127.0.0.1', 'root', 'root', 'flask')
        cursor = db.cursor(pymysql.cursors.DictCursor)  
        return db, cursor

    def get(self):
        db, cursor = self.db_init()

        sql = """
            select * from flask.accounts where deleted != True 
        """

        cursor.execute(sql)
        accounts = cursor.fetchall()
        db.close()

        response = {}
        response['code'] = 200
        response['msg'] = 'success'
        response['data'] = accounts

        return jsonify(response)

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        response = {}

        if arg["account_number"] == None and arg["user_id"] == None:
            response['code'] = 400
            response['msg'] = "account_number undetected"
            return jsonify(response)

        account = {
            "balance": arg["balance"],
            "account_number": arg["account_number"],
            "user_id": arg["user_id"]
        }
        sql = """
            Insert into flask.accounts(balance,account_number,user_id)
            Values('{}','{}','{}')
        """.format(account["balance"], account["account_number"], account["user_id"])
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


class Account(Resource):
    def db_init(self):
        db = pymysql.connect('127.0.0.1', 'root', 'root', 'flask')
        cursor = db.cursor(pymysql.cursors.DictCursor)  
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()

        sql = """
            select * from flask.accounts where id = '{}' and deleted != True
        """.format(id)

        cursor.execute(sql)
        accounts = cursor.fetchone() 
        db.close()

        response = {}
        response['code'] = 200
        response['msg'] = 'success'
        response['data'] = accounts

        return jsonify(response)

    def put(self, id):  
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            "balance": arg["balance"],
            "account_number": arg["account_number"],
            "user_id": arg["user_id"]
        }

        sql = """
            Update flask.accounts
            Set balance = "{}" , account_number = "{}" , user_id = "{}"
            Where id = {} and deleted != True
        """.format(account["balance"], account["account_number"], account["user_id"], id)

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

    def patch(self, id):  
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            "balance": arg["balance"],
            "account_number": arg["account_number"],
            "user_id": arg["user_id"]
        }

        query = []
        for key, value in account.items():
            if value != None:
                query.append(key + " = '{}' ".format(value))

        query = ",".join(query)

        sql = """
            Update flask.accounts
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



    def delete(self, id):  
        db, cursor = self.db_init()

        sql = """
            Update flask.accounts
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
