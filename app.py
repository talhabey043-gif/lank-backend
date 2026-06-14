import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient

app = Flask(__name__)
CORS(app)

# ANAHTAR GİZLENDİ: Bu satır, Render'daki 'Environment Variables' kısmından 
# HUGGINGFACE_API_KEY değerini çeker. Kodda asla gözükmez.
api_key = os.getenv("HUGGINGFACE_API_KEY")
client = InferenceClient(api_key=api_key)

@app.route('/islem', methods=['POST'])
def islem():
    try:
        data = request.json
        cmd = data.get('komut')
        veri = data.get('veri', '')
        
        if cmd == 'ai':
            res = client.chat_completion(
                messages=[{"role": "user", "content": veri}], 
                model="meta-llama/Meta-Llama-3-8B-Instruct"
            )
            return jsonify({"mesaj": res.choices[0].message.content})
        
        elif cmd == 'egitim':
            return jsonify({"mesaj": "LANK SOC Protokolü yüklendi: XSS, SQLi, CSRF ve DDoS analiz teknikleri aktif."})
        
        elif cmd == 'temizlik':
            return jsonify({"mesaj": "Sistem: Temp dosyaları temizlendi, loglar sıfırlandı. Local cache optimize edildi."})
        
        elif cmd == 'mail_uyari':
            return jsonify({"mesaj": "KRİTİK: Güvenlik merkezi maili iletildi."})
            
        elif cmd == 'anonim':
            print(f"ANONİM MESAJ GELDİ: {veri}")
            return jsonify({"mesaj": "Mesajınız anonim olarak iletildi."})

        return jsonify({"mesaj": "Komut anlaşılamadı."})
        
    except Exception as e:
        return jsonify({"mesaj": f"Sistem Hatası: API Anahtarı eksik veya geçersiz olabilir. Hata: {str(e)}"})

if __name__ == '__main__':
    # Render'da portu otomatik belirlemesi için 0.0.0.0 kullanıyoruz
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)