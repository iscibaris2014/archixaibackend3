from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="sk-...")  # SECRET KEY kullan

users = {}  # basit kullanıcı veritabanı (dict)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if email in users:
        return jsonify({"success": False, "message": "Bu e-posta zaten kayıtlı!"})
    users[email] = password
    return jsonify({"success": True, "message": "Kayıt başarılı!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if users.get(email) == password:
        return jsonify({"success": True, "message": "Giriş başarılı!"})
    return jsonify({"success": False, "message": "E-posta veya şifre hatalı!"})

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    if email in users:
        return jsonify({"success": True, "message": "Şifre sıfırlama maili gönderildi!"})
    return jsonify({"success": False, "message": "Bu e-posta kayıtlı değil!"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    
    answer = response.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
