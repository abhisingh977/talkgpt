from flask import Flask, jsonify, request, render_template
# from transformers import GPT2Tokenizer, GPT2LMHeadModel

app = Flask(__name__)

# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# model = GPT2LMHeadModel.from_pretrained("/home/abhishek/abhi/gita/iss/good_model/checkpoint-4000-1")
#     # "/home/abhishek/abhi/gita/iss/good_model/checkpoint-3000-2"

max_length = 75

@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/process-message", methods=["POST"])
# def process_text():
#     text = request.json["message"]
#     # response = {'message': 'I received your message: ' + text}
#     print(text)


#     inputs = tokenizer.encode(text, return_tensors="pt")
#     outputs = model.generate(
#         inputs,
#         do_sample=True,
#         max_new_tokens=max_length,
#         pad_token_id=model.config.eos_token_id,
#         top_k=50,
#         early_stopping=True,
#         top_p=0.95,
#         repetition_penalty=50.0,
#     )

#     generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     data = {"message": generated_text[len(text):]}

    # return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
