import json
import binance
from binance import Client
from flask import Flask, request,render_template

import config

app = Flask(__name__)
# client = Client(config.API_KEY, config.API_SECRET, tld='us')
# client = Client(config.API_KEY, config.API_SECRET)
client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity, symbol,order_type=binance.enums.ORDER_TYPE_MARKET):
    try:
        print(f"sending order {side} - {symbol} - {quantity} api - {config.API_KEY}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        error=(f"sending order {side} - {symbol} - {quantity} an exception occured - {e}")
        print(error)
        return error

    return order


@app.route("/")
def hello_world():
    return render_template('welcome.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    response=  order(data['strategy']['order_action'].upper(),"100",data['ticker'].upper())
    print({
        "code": "success" ,
        "order-executed": response,
        "Message": data
    })
    return {
        "code": "success" ,
        "order-executed": response,
        "Message": data
    }
