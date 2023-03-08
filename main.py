from flask import Flask, jsonify, request, render_template
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
app = Flask(__name__)

tokenizer = GPT2Tokenizer.from_pretrained("/app/model/")
model = GPT2LMHeadModel.from_pretrained("/app/model/")
#     # "/home/abhishek/abhi/gita/iss/good_model/checkpoint-3000-2"



@app.route("/")
def index():
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def chat():
    max_length = 50

    data = request.json
    text = data.get('text')
    print(text)
    inputs = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(
    inputs,
    do_sample=True,
    max_new_tokens=max_length,
    pad_token_id=model.config.eos_token_id,
    top_k=20,
    early_stopping=True,
    top_p=0.95,
    repetition_penalty=5.0,
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(generated_text[len(text):])
    # Return the response as JSON
    return jsonify({'response': generated_text[len(text):]})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

