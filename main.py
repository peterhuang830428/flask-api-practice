import flask
from flask import request, jsonify
import pymysql
from flask_restful import Api, Resource
from resource.user import Users, User
from resource.account import Accounts, Account

app = flask.Flask(__name__)
app.config["DEBUG"] = True

api = Api(app)
api.add_resource(Users, "/users")
api.add_resource(User, "/user/<id>")
api.add_resource(Accounts, "/accounts")
api.add_resource(Account, "/account/<id>")


@app.route('/', methods=['GET'])
def home():
    return "Hello World"


@app.before_request  # 早訪所有網頁前都一定要執行此部分
def auth():
    token = request.headers.get('auth')
    if token == '567':  # 通常會在前面先自動給加密token，不會寫死
        pass
    else:
        return {"code": 401, "msg": "invalid token"}


@app.errorhandler(Exception)  # 避免跳錯時會透露程式碼給使用者，因此要用較無緊要的訊息取代
def handle_error(error):
    status_code = 500
    if type(error).__name__ == "NotFound":
        status_code = 404

    return {"code": status_code, "msg": type(error).__name__}


@app.route('/account/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values["money"]  # 從html(ex:body)抓money的參數
    balance = account["balance"] + int(money)
    sql = """
        Update flask.accounts
        Set balance = '{}'
        Where account_number = '{}' and deleted != True
    """.format(balance, account["account_number"])
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


@app.route('/account/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values["money"]  # 從html(ex:body)抓money的參數
    balance = account["balance"] - int(money)

    response = {}
    if balance < 0:
        response['code'] = 400
        response['msg'] = 'money is not enough'
        return jsonify(response)

    sql = """
        Update flask.accounts
        Set balance = '{}'
        Where account_number = '{}' and deleted != True
    """.format(balance, account["account_number"])
    result = cursor.execute(sql)
    db.commit()
    db.close()

    if result == 0:
        response['code'] = 500
        response['msg'] = 'error'
    else:
        response['code'] = 200
        response['msg'] = 'success'

    return jsonify(response)


def get_account(account_number):
    db = pymysql.connect('127.0.0.1', 'root', 'root', 'flask')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
        Select * From flask.accounts where account_number = '{}'
    """.format(account_number)
    cursor.execute(sql)
    db.commit()
    return db, cursor, cursor.fetchone()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
