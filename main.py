from flask import Flask, render_template, jsonify, request
from openai import OpenAI
from flask_pymongo import PyMongo
#import pdb



#chatgpt open ai key(personal)
client = OpenAI(
    # This is the default and can be omitted
    api_key="Open AI API Key"
)

app = Flask(__name__)
app.config["MONGO_URI"] = "MongoDB API Key"
mongo = PyMongo(app)

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    #print(myChats)
    return render_template("index.html", myChats = myChats)
 

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        print(chat)
        #pdb.set_trace()
        if chat:
            data = {"question": question, "answer": f"{chat['answer']}"}
            return jsonify(data)
        else:
            response = client.chat.completions.create(
                 model="gpt-3.5-turbo",
                 messages=[
                     {
                     "role": "user",
                     "content": question
                     }
                 ],
                 temperature=1,
                 max_tokens=256,
                 top_p=1,
                 frequency_penalty=0,
                 presence_penalty=0)
            #response = ChatCompletion(id='chatcmpl-9F2YzzEXZnntEC0PTTTXyT8PSEAwK', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='4', role='assistant', function_call=None, tool_calls=None))], created=1713371801, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint='fp_c2295e73ad', usage=CompletionUsage(completion_tokens=1, prompt_tokens=10, total_tokens=11))
        #pdb.set_trace()    
        print(response)
        data = {"question": question, "answer": response.choices[0].message.content}
        mongo.db.chats.insert_one({"question": question, "answer": response.choices[0].message.content})

        return jsonify(data)
    data = {"result": "Thank you! I'm just a machine learning model designed to respond to questions and generate text based on my training data. Is there anything specific you'd like to ask or discuss? "}

    return jsonify(data)

app.run(debug=True)