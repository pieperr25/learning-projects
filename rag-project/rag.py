import chromadb
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('ANTHROPIC_API_KEY')

client1 = Anthropic(api_key=key)
client = chromadb.Client()
collection = client.create_collection(name="my_collection")

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

chunks = [i for i in chunks_old if len(i) > 100]

collection.add(
    ids=[str(i) for i in range(len([c for c in chunks if c.strip()]))],
    documents=chunks
)


while True:
    question = input('Question:')
    chunk = collection.query(
        query_texts=[question],
        n_results=5
    )

    message = client1.messages.create(
        max_tokens=1024,
        messages=[{'role':'user','content':f'Here is the context:{chunk['documents'][0]} Based on this, answer: {question}'}],
        model='claude-sonnet-4-6',
        system='Answer the questions based on only the context provided.'
    )
    print(message.content[0].text)
