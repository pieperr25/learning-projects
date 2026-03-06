import os
from anthropic import Anthropic
from dotenv import load_dotenv
import requests
import yfinance as yf


load_dotenv()

key = os.getenv('ANTHROPIC_API_KEY')

client = Anthropic(
    api_key=key
)

history = []

def ticker_request(ticker:str):
    ticker_data = yf.Ticker(ticker).info
    current_price = ticker_data.get('currentPrice') or ticker_data.get('regularMarketPrice')
    open_price = ticker_data.get('open')
    change = ((current_price-open_price)/open_price) *100
    return (f'{ticker}: Current Price{current_price}, Open Price: {open_price}, Day Change: {change}')

def claude_call(history:list):
        message = client.messages.create(
        max_tokens=1024,
        messages=history,
        model="claude-sonnet-4-6",
        system='You are a financial advisor. Evaluate stocks and provide your trading reccomendation with the goal of maximising the risk/reward ration. Perform a technical and fundamental analysis of the stock picks. The output formate should be in simple buy/sell, your projected performance on a scale of 1-10, and a short 2-3 sentences summary on the reasoning. Inform the user that this is not real finacial advice.',
        tools=[
    {
        "name": "get_stock_data",
        "description": "Gets current stock price data for a given ticker symbol",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol"
                }
            },
            "required": ["ticker"]
        }
    }
]
    )
        return message
while True:
    mess = input('User input:')
    history.append({'role':'user','content':mess})
    message = claude_call(history)
    history.append({'role':'assistant','content':message.content})
    for i in message.content:
        if i.type == 'tool_use':
            block_id = i.id
            block_input = i.input
            stock_data = ticker_request(block_input['ticker'])
            history.append({"role": "user", "content": [
    {
        "type": "tool_result",
        "tool_use_id": block_id,
        "content": stock_data
    }]})
            message = claude_call(history)
            history.append({'role':'assistant','content':message.content})


    print(message.content)