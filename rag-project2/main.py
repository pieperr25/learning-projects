import os
from anthropic import Anthropic
import chromadb
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()
key = os.getenv('ANTHROPIC_API_KEY')

client = Anthropic(api_key=key)
rag_client = chromadb.Client()
collection = rag_client.create_collection(name='rag_collection')

chunks_old = []
files = ['/Users/pieps/Documents/Obsidian/templates/principles/Mental Accounting.md',
'/Users/pieps/Documents/Obsidian/templates/entries/Overconfidence Bias.md',
'/Users/pieps/Documents/Obsidian/templates/entries/Anchoring.md',
'/Users/pieps/Documents/Obsidian/templates/entries/Status Quo Bias.md',
'/Users/pieps/Documents/Obsidian/templates/entries/Loss Aversion.md']

for i in files:
    with open(i,'r') as new:
        words = new.read()
        chunks_old.extend(words.split('\n\n'))

history = []
chunks = [i for i in chunks_old if len(i) > 100]

collection.add(
    ids=[str(i) for i in range(len([c for c in chunks if c.strip()]))],
    documents=chunks
    )

def rag_querry(data):
    chunk = collection.query(
    query_texts=[data],
    n_results=5
    )
    return chunk

def ticker_request(ticker):
    ticker_data = yf.Ticker(ticker).info
    current_price = ticker_data.get('currentPrice') or ticker_data.get('regularMarketPrice')
    open_price = ticker_data.get('open')
    change = ((current_price - open_price) / open_price) * 100
    return(f'{ticker}: Current price: {current_price}; Market open: {open_price}; Day change: {change}')

def claude_call(history:list):
        message = client.messages.create(
        max_tokens=1024,
        model='claude-sonnet-4-6',
        messages=history,
        system='Answer the question and use whatever tools necessary to complete the task',
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
    }, {
        "name": "query_knowledge_base",
        "description": "RAG data from behavioral economics knowledge base",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Most relevant knowledge"
                }
            },
            "required": ["query"]
        }}])
        return message

def tool_use(history:list,result:list):

    history.append({"role": "user", "content": result})
    message = claude_call(history)
    history.append({'role':'assistant','content':message.content})
    return(history,message)

while True:
    data = input('Comapny analytics: ')
    history.append({'role':'user','content':data})
    message = claude_call(history)
    history.append({'role':'assistant','content':message.content})


    while any(i.type == 'tool_use' for i in message.content):
        results = []
        for i in message.content:
            if i.type == 'tool_use':
                if i.name == 'get_stock_data':
                    results.append({'type':'tool_result','tool_use_id':i.id,'content':ticker_request(i.input['ticker'])})

                elif i.name == 'query_knowledge_base':
                    results.append({'type':'tool_result','tool_use_id':i.id,'content':str(rag_querry(i.input['query']))})

        history,message = tool_use(history,result)




    print(message.content)
