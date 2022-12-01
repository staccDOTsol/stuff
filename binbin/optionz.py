import asyncio
import json

import requests 
import numpy as np
from scipy.stats import norm
import datetime as dt
N = norm.cdf

import asyncio
import threading
import ccxt.async_support as ccxt



def BS_CALL(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * N(d1) - K * np.exp(-r*T)* N(d2)

def BS_PUT(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma* np.sqrt(T)
    return K*np.exp(-r*T)*N(-d2) - S*N(-d1)
import os
from time import sleep
async def test(loop):
    binance = ccxt.binance({
        'asyncio_loop': loop,  # ←---------------------------- ADDED THIS
        'enableRateLimit': True,  # ←---------------------------- ADDED THIS,
        'apiKey':'keoBAocR1AnQmuBbWZfsOOqPM2orVkWzyJQzbvbtfE6AzsScuVHsvZixytERB7Ad',
    'secret': os.environ["secret"]})
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'BTCUSDT'})
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'BNBUSDT'})
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'ETHUSDT'})
    sleep(3)
    req = (await binance.eapiPublicGetTicker())
    req2 = requests.get("https://eapi.binance.com/eapi/v1/mark").json()
    ethusdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()
    ethusdt =float( ethusdt['price'] )
    bnbusdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT").json()
    bnbusdt = float(bnbusdt['price'])
    btcusdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
    btcusdt = float(btcusdt['price'])
    ran = random.randint(0,100)
    if ran <= 10    :
        
        sleep(10)
        await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'BTCUSDT'})
        await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'BNBUSDT'})
        await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'ETHUSDT'})
    bal  = await binance.eapiPrivateGetAccount()
    
    oppstarts = []
    symoppstarts = []
    costs = []
    statestarts = []
    t = 0
    bbo2s = {}
    for m in req: 
        books = await binance.eapiPublicGetDepth({"symbol": m['symbol']})
        if len(books['bids']) >= 3:
            if(float(books['bids'][1][0]) - float(books['bids'][2][0]) > 2 * float(books['bids'][0][0]) - float(books['bids'][1][0])):
                print('newp')
                continue

            start = m['symbol'].split('-')[1]#dt.datetime(2010,1,1)    
            start = dt.datetime(int("20"+start[0:2]),int(start[2:4]),int(start[4:6]))
            now = dt.datetime.now()
            start = start - now 

            start = start.days / 365
            mp = ethusdt 
            if 'BNB' in m['symbol']:
                mp = bnbusdt 
            if 'BTC' in m['symbol']:
                mp = btcusdt
            ran = random.randint(0,10)
            price = float(m['bidPrice'])
            
            for m2 in req2: 
                #print(m2)
                if m2['symbol'] == m['symbol']:
                    markIv = m2['markIV']
            if start * 365 > 1 and price > 0:
                strike = float(m['symbol'].split('-')[-2])
                
                if '-P' in m['symbol']:
                    bc = (BS_PUT(mp, strike, 0.1, start, float(   markIv)))
                else: 
                    bc = (BS_CALL(mp, strike, 0.1, start, float(markIv)))
                try:
                    opp = ((     bc / price ) -1 ) * 100
                    print(opp)
                    if opp > 0:
                        
                        """
                        sleep(3)
                        t = threading.Thread(target=(print_poloniex_ethbtc_ticker), args=(m['symbol'],('underlying cost bc opp', mp, float(m['markPrice']), bc, str(round(opp))+'%'),))
                        t.daemon = True  
                        t.start()
                        """
                        statestarts.append((m['symbol'],('underlying cost bc opp opp APY', mp, float(m['bidPrice']), bc, str(round(opp))+'%'),str(round(opp*start))+'%'))
                        oppstarts.append(opp*start)
                        costs.append(float(m['bidPrice']))
                        symoppstarts.append(m['symbol'])
                        t = t + opp*start
                except Exception as e :
                    print(e)
    avg = t / len(oppstarts)
    t = 0
    c = 0
    relative = {}
    #print(avg)
    costs2 = {}
    oppstarts2 = []
    symoppstarts2 = []
    for i in range(0,len(oppstarts)):
        if float(oppstarts[i]) > 0:#avg / 3.333:
            t = t + oppstarts[i]
            oppstarts2.append(oppstarts[i])
            symoppstarts2.append(symoppstarts[i])
            c = c + 1
            #print(symoppstarts[i], oppstarts[i])
            #print(statestarts[i])
    avg = t / c 
    l = 0 
    s = 9999999999999999999999999
    for i in range(0,len(oppstarts2)):
        costs2[symoppstarts[i]]=(costs[i])
        relative[symoppstarts[i]] = (oppstarts2[i] / t) * 100
        if  (oppstarts2[i] / t) * 100 < s:
            s =  (oppstarts2[i] / t) * 100 
        if  (oppstarts2[i] / t) * 100 > l :
            l =  (oppstarts2[i] / t) * 100
    t = t - l - s 
    trelative = {}
    tcosts2 = {}
    for i in range (0, len(oppstarts2)):
        if  (oppstarts2[i] / t) * 100 != l and  (oppstarts2[i] / t) * 100 != s:
            tcosts2[symoppstarts[i]]=(costs[i])
            trelative[symoppstarts[i]] = (oppstarts2[i] / t) * 100
    relative = trelative 
    costs2 = tcosts2
    #print(relative)
    #print(avg)
    check = 0 
    for value in relative.values(): 
        check = check + value 
    #print(check)
    bal = float(bal['asset'][0]['available'])
    bal = bal #* 1.5# * 2 #/ 1.5
    print(bal)
    wanted = {} 
    
    for r in relative:
        inversetick = 1 / steps2[r][0]
        print(inversetick)
        if steps2[r][1] > 0:  
            inversetick = 1 / (steps2[r][0] * steps2[r][1])
        print(inversetick)
        #inversetick = 100
        if  (round(((relative[r] / 100) * bal) / costs2[r]  * inversetick)) / inversetick> 0:
            wanted[r] = (round(((relative[r] / 100) * bal) / costs2[r]  * inversetick)) / inversetick
  
    print(wanted)
    sleep(3)
    pos = await binance.eapiPrivateGetPosition()
    poses = {}
    for p in pos:
        poses[(p['symbol'])] = p
    
    sleep(3)
    oo = await binance.eapiPrivateGetOpenOrders()
    openos = {}
    for p in oo:
        openos[(p['symbol'])] = p
        
    for want in wanted:
        try:
            if True:#want not in openpos:
                
                r = want 

                price = costs2[want] + steps[want][0]
                print(price)
                if steps[want][1] > 0:  
                    price = costs2[want] +( steps[want][0] * steps[want][1] )
                print(price)
                inversetick = 1 / steps[r][0]
                print(inversetick)
                if steps[r][1] > 0:  
                    inversetick = 1 / (steps[r][0] * steps[r][1])
                print(inversetick)
                #inversetick = 100
                
                price = (round(price  * inversetick)) / inversetick
                if want in openos:

                    if openos[want]['side'] == 'BUY':
                        if float(openos[want]['price']) != float(costs2[want]):

                            c = await binance.eapiPrivateDeleteOrder({'symbol': want, "orderId": openos[want]['orderId']})
                            print(c)
                elif price > 0:
                    sleep(0.01)
                    order = await binance.eapiPrivatePostOrder({
                        "symbol": want,
                        "side": "BUY",
                        "type": "LIMIT",
                        "postOnly": True,
                        "quantity": wanted[want] ,
                        "price": price

                    })
                    print(order)
                
                abc=123
        except Exception as e :
            print(e)
    print(statestarts)
    await binance.close()  # ←---------------------------- ADDED THIS


async def monye(loop):
    binance = ccxt.binance({
        'asyncio_loop': loop,  # ←---------------------------- ADDED THIS
        'enableRateLimit': True,  # ←---------------------------- ADDED THIS,
        'apiKey':'keoBAocR1AnQmuBbWZfsOOqPM2orVkWzyJQzbvbtfE6AzsScuVHsvZixytERB7Ad',
    'secret': os.environ["secret"]})
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'BTCUSDT'})
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'BNBUSDT'})
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'ETHUSDT'})
    sleep(3)
    req = (await binance.eapiPublicGetTicker())
    req2 = requests.get("https://eapi.binance.com/eapi/v1/mark").json()
    ethusdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()
    ethusdt =float( ethusdt['price'] )
    bnbusdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT").json()
    bnbusdt = float(bnbusdt['price'])
    btcusdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
    btcusdt = float(btcusdt['price'])
  
    sleep(3)
    pos = await binance.eapiPrivateGetPosition()
    poses = {}
    sleep(3)
    req = (await binance.eapiPublicGetTicker())
    for r in req:
        for p in pos:
            if p['symbol'] == r['symbol']:
                p['askPrice'] = r['askPrice']
                poses[(p['symbol'])] = p
    sleep(3)
    oo = await binance.eapiPrivateGetOpenOrders()
    openos = {}
    for p in oo:
        openos[(p['symbol'])] = p
    for want in poses:
        try:
            #if True:#want not in openpos:
            books = await binance.eapiPublicGetDepth({"symbol": want})
            if len(books['asks']) >= 3:
                if( float(books['asks'][2][0]) - float(books['asks'][1][0]) < 1.5 * float(books['asks'][1][0]) - float(books['asks'][0][0])):
                    print('newp ask')
                    continue
                r = want 
                poses[want]['askPrice'] = float(poses[want]['askPrice'])
                price = poses[want]['askPrice']
                if want in openos:
                    if openos[want]['side'] == 'SELL':
                        if True:#float(openos[want]['price']) != float(price):

                            c = await binance.eapiPrivateDeleteOrder({'symbol': want, "orderId": openos[want]['orderId']})
                            print(c)

                else:
                    try:
                            
                        order = await binance.eapiPrivatePostOrder({
                                "symbol": poses[want]['symbol'],
                                "side": "SELL",
                                "type": "LIMIT",
                        "postOnly": True,
                                "quantity": float(poses[want]['quantity']) / 2,
                                "price": price

                            })
                        print(order)
                    except Exception as e:
                        print(e)
                        order = await binance.eapiPrivatePostOrder({
                                "symbol": poses[want]['symbol'],
                                "side": "SELL",
                                "type": "LIMIT",
                                "quantity": poses[want]['quantity'],
                                "price": price

                            })
                        print(order)
                abc=123
        except Exception as e :
            print(e)
    await binance.close()  # ←---------------------------- ADDED THIS
steps = {}
steps2 = {}
import random 
async def setup(loop):
    global steps
    
    binance = ccxt.binance({
        'asyncio_loop': loop,  # ←---------------------------- ADDED THIS
        'enableRateLimit': True,
        'apiKey':'keoBAocR1AnQmuBbWZfsOOqPM2orVkWzyJQzbvbtfE6AzsScuVHsvZixytERB7Ad',
    'secret': os.environ["secret"]})    
    """t = await binance.eapiPrivatePostCountdownCancelAll({'underlying':
        'BTCUSDT',
    'countdownTime': 5000})    
    """
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'BTCUSDT'})
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'BNBUSDT'})
    #await binance.eapiPrivateDeleteAllOpenOrdersByUnderlying({'underlying': 'ETHUSDT'})
    info = await binance.eapiPublicGetExchangeInfo()
    print(info)
    symbols = info['optionSymbols']
    for sym in symbols:
        steps[sym['symbol']]=([float(sym['filters'][0]['tickSize']),float(float(sym['priceScale']))])
        steps2[sym['symbol']]=([float(sym['filters'][1]['stepSize']),float(float(sym['quantityScale']))])

    await binance.close()
    #print(t)
def functionInNewThread2():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(setup(loop))
def functionInNewThread():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test(loop))
def functionInNewThreadMonye():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(monye(loop))
thread = threading.Thread(target=functionInNewThread2)
thread.start()
thread.join()
while True:
    
    

    thread = threading.Thread(target=functionInNewThread2)
    thread.start()
    thread.join()
    thread = threading.Thread(target=functionInNewThreadMonye)
    thread.start()
    thread.join()

    thread = threading.Thread(target=functionInNewThread)
    thread.start()
    thread.join()

