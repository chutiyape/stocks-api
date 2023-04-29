from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'finance_data.db'


@app.route('/stocks/<string:date>', methods=['GET'])
def get_all_companies_stock_data(date):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM finance_data WHERE date=?", (date,))
    data = cur.fetchall()
    conn.close()
    return jsonify(data)




#http://localhost:5000/stocks/IBM/2022-04-29
@app.route('/stocks/<company_name>/<date>', methods=['GET'])
def get_company_stock_data_on_date(company_name, date):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM finance_data WHERE company=? AND date=?", (company_name, date))
    data = cur.fetchall()
    conn.close()
    return jsonify(data)

#http://localhost:5000/stocks?company_name=PAYTM.NS
@app.route('/stocks', methods=['GET'])
def get_company_stock_data():
    company_name = request.args.get('company_name')
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM finance_data WHERE company=?", (company_name,))
    
    data = cur.fetchall()
    conn.close()
    return jsonify(data)




@app.route('/stocks/<company_id>', methods=['POST', 'PATCH'])
def update_stock_data(company_id):
    date = request.json['date']
    open_price = request.json['open']

    high_price = request.json['high']
    low_price = request.json['low']
    close_price = request.json['close']

    adj_close_price = request.json['adj_close']



    volume = request.json['volume']

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO finance_data (company, date, open, high, low, close, adj_close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(company, date) DO UPDATE SET
        open = excluded.open,
        high = excluded.high,
        low = excluded.low,
        close = excluded.close,
        adj_close = excluded.adj_close,
        volume = excluded.volume
    ''', (company_id, date, open_price, high_price, low_price, close_price, adj_close_price, volume))
    conn.commit()
    conn.close()


    return jsonify({'message': 'data updated successfully.'})

if __name__ == '__main__':
    app.run()



''' {
    "date": "2023-01-01",
    "open": 150.0,
    "high": 155.0,
    "low": 140.0,
    "close": 145.0,
    "adj_close": 143.0,
    "volume": 1000000
}

curl --location --request POST 'http://localhost:5000/stocks/IBM' \
--header 'Content-Type: application/json' \
--data-raw '{
    "date": "2023-01-01",
    "open": 150.0,
    "high": 155.0,
    "low": 140.0,
    "close": 145.0,
    "adj_close": 143.0,
    "volume": 1000
}'
'''

