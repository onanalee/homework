from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')

# 주문하기 API (POST)
@app.route('/order', methods=['POST'])
def save_order():

    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    # DB에 삽입할 review 만들기
    candle = {
        'name': name_receive,
        'count': count_receive,
        'address': address_receive,
        'phone': phone_receive
    }
    # reviews에 review 저장하기
    db.candles.insert_one(candle)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})


#주문 목록보기 API (read)
@app.route('/order',methods=['GET'])
def view_orders():
    # 1. DB에서 리뷰 정보 모두 가져오기
    candles= list(db.candles.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'candles': candles})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)