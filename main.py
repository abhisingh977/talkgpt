from flask import Flask, jsonify, request, render_template, session
import os
import uuid
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
app = Flask(__name__)
import logging

tokenizer = AutoTokenizer.from_pretrained("model/")
model = AutoModelForCausalLM.from_pretrained("model/")

app.secret_key = str(uuid.uuid1())
def crop_sentence(sentence):
    counter = 0
    current_substring = ""
    for char in reversed(sentence):
        current_substring += char
        if char == ".":
            counter += 1
            if counter == 6:
                sentence = current_substring[::-1]
                return sentence[2:]
                

    return sentence




@app.route("/")
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    text = data.get('text')

    print("text")
    print(text)

    # Check if there is an existing chat history in the session
    chat_history_ids = session.get('chat_history_ids')
    if chat_history_ids is None:
        chat_history_ids = torch.tensor([])
    else:
        chat_history_ids = torch.tensor(chat_history_ids)

    if len(chat_history_ids) > 0:
        text = " " +text
        chat_history_text = tokenizer.decode(chat_history_ids[0], skip_special_tokens=True, padding_side='left')
        chat_history_ids = tokenizer.encode(crop_sentence(chat_history_text) + tokenizer.eos_token, return_tensors='pt')

    else:
        text = text



    # Generate a new response using the chat history
    new_user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')

    bot_input_ids = torch.cat([chat_history_ids , new_user_input_ids], dim=-1) if len(chat_history_ids) > 0 else new_user_input_ids
    print("bot_input_ids")
    print(tokenizer.decode(bot_input_ids[0], skip_special_tokens=True, padding_side='left'))



    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    generated_text = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True, padding_side='left')
    print("generated_text")
    print(generated_text)
    chat_history_list = chat_history_ids.tolist()
    # Store the updated chat history in the session
    session['chat_history_ids'] = chat_history_list

    # Return the response as JSON
    return jsonify({'response': str(generated_text)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

