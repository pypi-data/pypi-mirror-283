import os
from dotenv import load_dotenv
load_dotenv()
import httpx
import asyncio
from .trader_models.trader_models import Capital, DT_DAY_DETAIL_LIST, Positions, OpenPositions, OrderHistory
from polygonio.polygon_database import PolygonDatabase
from typing import Optional
account_id = os.environ.get('webull_account_id')
from datetime import datetime, timedelta

from .trader_models.trader_models import OptionData

class PaperTrader:
    def __init__(self):
        self.id = 15765933
        self.headers  = {
        "Accept": os.getenv("ACCEPT"),
        "Accept-Encoding": os.getenv("ACCEPT_ENCODING"),
        "Accept-Language": "en-US,en;q=0.9",
        'Content-Type': 'application/json',
        "App": os.getenv("APP"),
        "App-Group": os.getenv("APP_GROUP"),
        "Appid": os.getenv("APPID"),
        "Device-Type": os.getenv("DEVICE_TYPE"),
        "Did": 'gldaboazf4y28thligawz4a7xamqu91g',
        "Hl": os.getenv("HL"),
        "Locale": os.getenv("LOCALE"),
        "Origin": os.getenv("ORIGIN"),
        "Os": os.getenv("OS"),
        "Osv": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Ph": os.getenv("PH"),
        "Platform": os.getenv("PLATFORM"),
        "Priority": os.getenv("PRIORITY"),
        "Referer": os.getenv("REFERER"),
        "Reqid": os.getenv("REQID"),
        "T_time": os.getenv("T_TIME"),
        "Tz": os.getenv("TZ"),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Ver": os.getenv("VER"),
        "X-S": os.getenv("X_S"),
        "X-Sv": os.getenv("X_SV")
    }
        #miscellaenous
                #sessions
        self._account_id = ''
        self._trade_token = ''
        self._access_token = ''
        self._refresh_token = ''
        self._token_expire = ''
        self._uuid = ''

        self._region_code = 6
        self.zone_var = 'dc_core_r001'
        self.timeout = 15
        self.db = PolygonDatabase(host='localhost', user='chuck', database='fudstop2', password='fud', port=5432)
        self.device_id = "gldaboazf4y28thligawz4a7xamqu91g"

    def to_decimal(self, value: Optional[str]) -> str:
        """
        Convert percentage string to decimal string if needed.
        """
        if value is not None and float(value) > 1:
            return str(float(value) / 100)
        return value


    async def get_token(self):
        endpoint = f"https://u1suser.webullfintech.com/api/user/v1/login/account/v2"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.post(endpoint, json={"account":"CHUCKDUSTIN12@GMAIL.COM","accountType":"2","pwd":"fb050b003c6d84da626a4f53f8a1b400","deviceId":"gldaboazf4y28thligawz4a7xamqu91g","deviceName":"Windows Chrome","grade":1,"regionId":1})
        data = data.json()
        token = data.get('accessToken')
        print(token)
        return token



    async def get_quote(self, ticker, db):
        async with semaphore:
            try:
                ticker_id = await trading.get_ticker_id(ticker)
                endpoint = f"https://quotes-gw.webullfintech.com/api/stock/tickerRealTime/getQuote?tickerId={ticker_id}&includeSecu=1&includeQuote=1&more=1"
                async with httpx.AsyncClient() as client:
                    data = await client.get(endpoint)
                    data = data.json()
                    # Updated data_dict


                    # Extracting data from the input dictionary
                    name = data.get('name', None)
                    symbol = data.get('symbol', None)
                    derivative_support = data.get('derivativeSupport', 0)
                    close = float(data.get('close', 0))
                    change = float(data.get('change', 0))
                    change_ratio = round(float(data.get('changeRatio', 0)) * 100, 2)
                    market_value = float(data.get('marketValue', 0))
                    volume = float(data.get('volume', 0))
                    turnover_rate = round(float(data.get('turnoverRate', 0)) * 100, 2)
                    open = float(data.get('open', 0))
                    high = float(data.get('high', 0))
                    low = float(data.get('low', 0))
                    vibrate_ratio = float(data.get('vibrateRatio', 0))
                    avg_vol_10d = float(data.get('avgVol10D', 0))
                    avg_vol_3m = float(data.get('avgVol3M', 0))
                    neg_market_value = float(data.get('negMarketValue', 0))
                    pe = float(data.get('pe', 0))
                    forward_pe = float(data.get('forwardPe', 0))
                    indicated_pe = float(data.get('indicatedPe', 0))
                    pe_ttm = float(data.get('peTtm', 0))
                    eps = float(data.get('eps', 0))
                    eps_ttm = float(data.get('epsTtm', 0))
                    pb = float(data.get('pb', 0))
                    total_shares = float(data.get('totalShares', 0))
                    outstanding_shares = float(data.get('outstandingShares', 0))
                    fifty_two_wk_high = float(data.get('fiftyTwoWkHigh', 0))
                    fifty_two_wk_low = float(data.get('fiftyTwoWkLow', 0))
                    dividend = float(data.get('dividend', 0))
                    yield_ = float(data.get('yield', 0))
                    latest_dividend_date = data.get('latestDividendDate', None)
                    latest_split_date = data.get('latestSplitDate', None)
                    latest_earnings_date = data.get('latestEarningsDate', None)
                    ps = float(data.get('ps', 0))
                    bps = float(data.get('bps', 0))
                    estimate_earnings_date = data.get('estimateEarningsDate', None)

                    # Calculate percentage from 52-week high
                    pct_from_52_high = ((fifty_two_wk_high - close) / fifty_two_wk_high) * 100 if fifty_two_wk_high != 0 else None

                    # Calculate percentage from 52-week low
                    pct_from_52_low = ((close - fifty_two_wk_low) / fifty_two_wk_low) * 100 if fifty_two_wk_low != 0 else None

                    # Calculate volume vs average volume (10 days)
                    volume_vs_avg_vol_10d = (volume / avg_vol_10d) if avg_vol_10d != 0 else None
                    volume_vs_avg_vol_10d = round(float(volume_vs_avg_vol_10d)* 100, 2)
                    # Calculate volume vs average volume (3 months)
                    volume_vs_avg_vol_3m = (volume / avg_vol_3m) if avg_vol_3m != 0 else None
                    volume_vs_avg_vol_3m = round(float(volume_vs_avg_vol_3m)* 100, 2)

                    # Create new earnings metrics
                    earnings_to_price = (eps_ttm / close) if close != 0 else None
                    earnings_to_price = round(float(earnings_to_price)*100,2)
                    forward_earnings_to_price = (forward_pe / close) if close != 0 else None
                    forward_earnings_to_price = round(float(forward_earnings_to_price) * 100, 2)

                    data_dict = {
                        'name': name,
                        'ticker': symbol,
                        'derivative_support': derivative_support,
                        'close': close,
                        'change': change,
                        'change_ratio': change_ratio,
                        'market_value': market_value,
                        'volume': volume,
                        'turnover_rate': turnover_rate,
                        'open': open,
                        'high': high,
                        'low': low,
                        'vibrate_ratio': vibrate_ratio,
                        'avg_vol_10d': avg_vol_10d,
                        'avg_vol_3m': avg_vol_3m,
                        'neg_market_value': neg_market_value,
                        'pe': pe,
                        'forward_pe': forward_pe,
                        'indicated_pe': indicated_pe,
                        'pe_ttm': pe_ttm,
                        'eps': eps,
                        'eps_ttm': eps_ttm,
                        'pb': pb,
                        'total_shares': total_shares,
                        'outstanding_shares': outstanding_shares,
                        'fifty_two_wk_high': fifty_two_wk_high,
                        'fifty_two_wk_low': fifty_two_wk_low,
                        'dividend': dividend,
                        'yield': yield_,
                        'latest_dividend_date': latest_dividend_date,
                        'latest_split_date': latest_split_date,
                        'latest_earnings_date': latest_earnings_date,
                        'ps': ps,
                        'bps': bps,
                        'estimate_earnings_date': estimate_earnings_date,
                        'pct_from_52_high': pct_from_52_high,
                        'pct_from_52_low': pct_from_52_low,
                        'volume_vs_avg_vol_10d': volume_vs_avg_vol_10d,
                        'volume_vs_avg_vol_3m': volume_vs_avg_vol_3m,
                        'earnings_to_price': earnings_to_price,
                        'forward_earnings_to_price': forward_earnings_to_price,

                    }

                    # Print to verify the updated dictionary
                
                    df = pd.DataFrame(data_dict, index=[0])

                    await db.batch_insert_dataframe(df, table_name='quote', unique_columns='ticker')

                    if volume_vs_avg_vol_10d >= 150:
                        data_dict.update({'status': 'above_avg_volume'})
                        color = hex_color_dict.get('green')
                        title = f"Above Average Volume - {data_dict.get('ticker')}"
                        await volume_embed(data_dict, above_avg_vol, color=color, title=title)


                    elif volume_vs_avg_vol_10d <= 25:
                        data_dict.update({'status': 'below_avg_volume'})
                        title = f"Below Average Volume - {data_dict.get('ticker')}"
                        color = hex_color_dict.get('red')
                        await volume_embed(data_dict, below_avg_vol, color=color, title=title)

                    if close == fifty_two_wk_high:
                        color = hex_color_dict.get('red')
                        title = f"NEW 52 WEEK HIGH - {data_dict.get('ticker')}"
                        await volume_embed(data_dict, color=color, hook=new_high, title=title)

                    if close == fifty_two_wk_low:
                        color = hex_color_dict.get('green')
                        title = f"NEW 52 WEEK LOW - {data_dict.get('ticker')}"
                        await volume_embed(data_dict, color=color, hook=new_low, title=title)


                    if change_ratio <= -10:
                        color = hex_color_dict.get('red')

                        title = f"SHORT SALE RESTRICTION - {data_dict.get('ticker')}"

                        await volume_embed(data_dict, color=color, title=title, hook=ssr_hook)


            except Exception as e:
                print(e)


    async def update_trade_token(self):
        payload = { 'pwd': '5ad14adc3d09d9517fecfb031e3676e9'}
        endpoint = f"https://u1suser.webullfintech.com/api/user/v1/security/login"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.post(endpoint, json=payload, headers=self.headers)
            data = data.json()
            token = data.get('tradeToken')
            
            return token
    

    async def get_account_detail(self, account_id:str=account_id):
        """Gets trading summary."""
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        endpoint = f"https://ustrade.webullfinance.com/api/trading/v1/webull/asset/summary?secAccountId={account_id}"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()
            print(data)
            capital = data['capital']

            return Capital(capital)
        

    async def profit_loss(self):
        endpoint=f"https://ustrade.webullfinance.com/api/trading/v1/webull/profitloss/account/getProfitlossAccountSummary?secAccountId=12165004&startDate=2024-04-19&endDate=2024-04-23"
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            return data


    async def get_option_data(self, option_ids):
        endpoint = f"https://quotes-gw.webullfintech.com/api/quote/option/quotes/queryBatch?derivativeIds={option_ids}"
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            return OptionData(data)


    async def positions(self):
        """RETURNS OPEN POSITIONS AND ACCOMPANYING DATA"""
        endpoint = f"https://ustrade.webullfinance.com/api/trading/v1/webull/asset/summary?secAccountId={account_id}"
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint, headers=self.headers)
            data = data.json()

            pos = data['positions']
            items = [i.get('items') for i in pos]
            items = [item for sublist in items for item in sublist]

            positions = Positions(data['positions'])

            open_positions = OpenPositions(items)

            option_ids = open_positions.tickerId

            option_ids_str = ','.join(map(str, option_ids))

            option_data = f"https://quotes-gw.webullfintech.com/api/quote/option/quotes/queryBatch?derivativeIds={option_ids_str}"

            async with httpx.AsyncClient() as client:
                data = await client.get(option_data, headers=self.headers)
                data = data.json()
                return open_positions, OptionData(data)




    async def get_order_history(self):

        """GETS ACCOUNT ORDER HISTORY
        
        RETURNS A TUPLE
        """


        endpoint = f"https://ustrade.webullfinance.com/api/trading/v1/webull/order/list?secAccountId=12165004"
        payload ={"dateType":"ORDER","pageSize":1000,"startTimeStr":"2024-04-01","endTimeStr":"2024-04-27","action":None,"lastCreateTime0":0,"secAccountId":12165004,"status":"all"}
        token = await self.update_trade_token()
        self.headers.update({"T_Token": token})
        async with httpx.AsyncClient() as client:

            data = await client.post(endpoint, headers=self.headers, json=payload)

            data = data.json()


            history_data =  OrderHistory(data)

            ticker_ids = history_data.tickerId

            tasks = [self.get_option_data(i) for i in ticker_ids]

            results = await asyncio.gather(*tasks)

            return history_data, results[0]