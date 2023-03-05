from flask import Flask, jsonify, request, render_template
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
app = Flask(__name__)

tokenizer = GPT2Tokenizer.from_pretrained("/app/model/")
model = GPT2LMHeadModel.from_pretrained("/app/model/")
#     # "/home/abhishek/abhi/gita/iss/good_model/checkpoint-3000-2"

max_length = 60

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process-message", methods=["POST"])
def process_text():
    chatbot_response = ""
    if data['response'] != '':
        chatbot_response = data['response']

    elif data['response'] == '':
        user_input = chatbot_response + data['message']
        print(user_input)
        inputs = tokenizer.encode(user_input, return_tensors="pt")
        outputs = model.generate(
            inputs,
            do_sample=True,
            max_new_tokens=max_length,
            pad_token_id=model.config.eos_token_id,
            top_k=30,
            early_stopping=True,
            top_p=0.95,
            repetition_penalty=20.0,
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)


        data = {"message": generated_text[len(text):]}

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

