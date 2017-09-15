from flask import Flask,jsonify,request
import json
import redis



app = Flask(__name__)


@app.route('/product',methods=['POST','GET'])
def get_newproduct():
    try:
        me = eval(request.json)
        tasks = me.get('tasks')
        name = me.get('name')
    except:
        tasks = request.json.get('tasks')
        name = request.json.get('name')

    r = redis.Redis(host='127.0.0.1', port=6379)

    str_tasks = str(tasks)[1:-1]
    exec("r.rpush(name,{})".format(str_tasks))

    return jsonify({'msg': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
