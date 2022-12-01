
import asyncio
import threading
import ccxt.async_support as ccxt
import os
from time import sleep 
stotal = 0
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def test(loop):
    global stotal
    binance = ccxt.binance({
        'asyncio_loop': loop,  # ←---------------------------- ADDED THIS
        'enableRateLimit': True,  # ←---------------------------- ADDED THIS,
        'apiKey':'keoBAocR1AnQmuBbWZfsOOqPM2orVkWzyJQzbvbtfE6AzsScuVHsvZixytERB7Ad',
    'secret': os.environ["secret"]})
    stuff = await binance.eapiPrivateGetBill({"currency": "USDT", 
    "limit": 1000})
    print(len(stuff))
    results = {}
    resultsneg = {}
    total = 0 
    ctotal = 0
    
    for s in stuff:
        if s['type'] not in results:
            results[s['type']] = 0 
            resultsneg[s['type']] = 0
        total = total + float(s['amount'])
        if float(s['amount']) < 0:
            resultsneg[s['type']] = resultsneg[s['type']] + float(s['amount'])
            
        else:
            results[s['type']] = results[s['type']] + float(s['amount'])

    pos = await binance.eapiPrivateGetPosition()
    poses = {}
    for i in range(0,100):
        print('')
    values = 0
    oo = await binance.eapiPrivateGetOpenOrders()
    openos = {}
    print('orders:')
    for p in oo:
        openos[(p['symbol'])] = p
        print(p['side'] + ' ' + p['symbol'] + ': $' + str(round(float(p['price']) * float(p['quantity']) * 100) / 100))
    print('')
    print('positions:')
    for p in pos:
        poses[(p['symbol'])] = p
        s = p['side']
        ror = p['ror']
        if float(ror) > 0:
            print(s + ' ' + p['symbol'] +': ' + bcolors.OKGREEN + str(ror) + '%, $' + str(p['unrealizedPNL']) + bcolors.ENDC)
        else:
            print(s + ' ' + p['symbol'] +': ' + bcolors.WARNING + str(ror) + '%, $' + str(p['unrealizedPNL']) + bcolors.ENDC)
        values = values + float(p['markValue'])
    print('')
    if stotal == 0:
        stotal = total + values
    print('net buys/sells last 1000 transactions: $', str(((round(resultsneg['CONTRACT'] * 100) / 100)+round(results['CONTRACT'] * 100) / 100)))

    print('net buys/sells since begginning this run: $ ' + str(round(((total + values)-stotal) * 100) / 100))
    print('wallet value: $' + str(round((values + total) * 100) / 100))
    print('positions value: $' + str(round(values * 100) / 100))
    print('margin balance: $' + str(round(total * 100) / 100))
    print('')
    print('deposits last 1000 transactions: $', str(round(results['TRANSFER'] * 100) / 100))
    print('withdraws last 1000 transactions: $', str(-1*round(resultsneg['TRANSFER'] * 100) / 100))
    print('fees last 1000 transactions: $', str(-1*round(resultsneg['FEE'] * 100) / 100))
    print('volume last 1000 transactions: $', str(((-1*round(resultsneg['CONTRACT'] * 100) / 100)+round(results['CONTRACT'] * 100) / 100)))
    await binance.close()
def functionInNewThreadMonye():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test(loop))
while True:
    
    thread = threading.Thread(target=functionInNewThreadMonye)
    thread.start()
    thread.join()
    sleep(60)