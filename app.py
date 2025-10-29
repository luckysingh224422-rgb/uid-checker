from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

GRAPH_API_URL = "https://graph.facebook.com/v18.0"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AAHAN UID CHECKER - VIP UID Finder</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    :root {
      --neon-cyan: #00ffff;
      --neon-pink: #ff00ff;
      --neon-blue: #0066ff;
      --neon-purple: #9d00ff;
      --vip-gold: #ffd700;
    }
    
    body {
      margin: 0;
      padding: 0;
      font-family: 'Rajdhani', sans-serif;
      background: 
        radial-gradient(circle at 20% 30%, rgba(255, 0, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 80%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
        linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 50%, #0a0a2a 100%);
      color: white;
      text-align: center;
      min-height: 100vh;
      overflow-x: hidden;
    }

    .vip-badge {
      position: absolute;
      top: 10px;
      right: 10px;
      background: linear-gradient(45deg, var(--vip-gold), #ff9500);
      color: black;
      padding: 5px 15px;
      border-radius: 20px;
      font-weight: bold;
      font-size: 12px;
      animation: pulse 2s infinite;
      transform: rotate(5deg);
    }

    .container {
      max-width: 450px;
      margin: 80px auto;
      background: rgba(10, 10, 30, 0.95);
      padding: 30px 25px;
      border-radius: 20px;
      border: 3px solid transparent;
      background-clip: padding-box;
      position: relative;
      backdrop-filter: blur(10px);
      box-shadow: 
        0 0 30px var(--neon-purple),
        inset 0 0 20px rgba(0, 255, 255, 0.1);
    }

    .container::before {
      content: '';
      position: absolute;
      top: -3px;
      left: -3px;
      right: -3px;
      bottom: -3px;
      background: linear-gradient(45deg, var(--neon-cyan), var(--neon-pink), var(--neon-blue), var(--neon-purple));
      border-radius: 23px;
      z-index: -1;
      animation: borderGlow 3s linear infinite;
    }

    @keyframes borderGlow {
      0% { filter: hue-rotate(0deg); }
      100% { filter: hue-rotate(360deg); }
    }

    .title {
      font-family: 'Orbitron', sans-serif;
      font-size: 32px;
      font-weight: 900;
      background: linear-gradient(45deg, var(--neon-cyan), var(--neon-pink), var(--vip-gold));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
      animation: titleGlow 2s ease-in-out infinite alternate;
      margin-bottom: 30px;
      letter-spacing: 2px;
    }

    @keyframes titleGlow {
      0% { text-shadow: 0 0 20px rgba(0, 255, 255, 0.7); }
      100% { text-shadow: 0 0 30px rgba(255, 0, 255, 0.7), 0 0 40px rgba(255, 0, 255, 0.4); }
    }

    .subtitle {
      font-size: 14px;
      color: var(--neon-cyan);
      margin-bottom: 25px;
      font-weight: 300;
      letter-spacing: 1px;
    }

    input[type="text"] {
      width: 90%;
      padding: 15px;
      border-radius: 12px;
      border: 2px solid transparent;
      background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(50, 50, 80, 0.6));
      color: white;
      font-size: 16px;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 500;
      transition: all 0.3s ease;
      box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    }

    input[type="text"]:focus {
      outline: none;
      border: 2px solid var(--neon-cyan);
      box-shadow: 0 0 20px var(--neon-cyan), inset 0 0 10px rgba(0, 255, 255, 0.2);
      transform: scale(1.02);
    }

    input[type="text"]::placeholder {
      color: rgba(255, 255, 255, 0.6);
    }

    .button-group {
      position: relative;
      margin-top: 25px;
    }

    button {
      padding: 14px 35px;
      font-size: 16px;
      font-family: 'Orbitron', sans-serif;
      font-weight: 700;
      border: none;
      background: linear-gradient(45deg, var(--neon-blue), var(--neon-purple));
      color: white;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
      letter-spacing: 1px;
      box-shadow: 0 0 20px rgba(157, 0, 255, 0.5);
    }

    button:hover {
      transform: translateY(-3px) scale(1.05);
      box-shadow: 0 0 30px var(--neon-purple), 0 5px 15px rgba(0, 0, 0, 0.3);
    }

    button:active {
      transform: translateY(1px);
    }

    button::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      transition: 0.5s;
    }

    button:hover::before {
      left: 100%;
    }

    .result-container {
      margin-top: 30px;
      max-height: 300px;
      overflow-y: auto;
      padding-right: 10px;
    }

    .result-container::-webkit-scrollbar {
      width: 5px;
    }

    .result-container::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.3);
      border-radius: 10px;
    }

    .result-container::-webkit-scrollbar-thumb {
      background: linear-gradient(var(--neon-cyan), var(--neon-purple));
      border-radius: 10px;
    }

    .result-item {
      margin-top: 15px;
      padding: 15px;
      background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
      border: 1px solid transparent;
      border-radius: 12px;
      animation: resultAppear 0.5s ease-out;
      position: relative;
      backdrop-filter: blur(5px);
      box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
    }

    @keyframes resultAppear {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .result-item::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    }

    .result-item strong {
      color: var(--vip-gold);
      font-size: 18px;
      font-family: 'Orbitron', sans-serif;
      display: block;
      margin-bottom: 8px;
    }

    .result-item .uid {
      color: var(--neon-cyan);
      font-family: 'Rajdhani', sans-serif;
      font-weight: 500;
      font-size: 16px;
    }

    .error-message {
      background: linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(255, 0, 255, 0.1));
      border: 1px solid rgba(255, 0, 0, 0.5);
      color: #ff6b6b;
      padding: 15px;
      border-radius: 12px;
      margin-top: 20px;
      animation: shake 0.5s ease-in-out;
    }

    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-5px); }
      75% { transform: translateX(5px); }
    }

    .footer-box {
      margin-top: 30px;
      padding: 15px;
      background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(0, 255, 255, 0.1));
      border: 1px solid transparent;
      border-radius: 12px;
      font-weight: bold;
      font-size: 15px;
      font-family: 'Orbitron', sans-serif;
      position: relative;
      overflow: hidden;
      box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }

    .footer-box::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: conic-gradient(transparent, rgba(255, 215, 0, 0.3), transparent 30%);
      animation: rotate 4s linear infinite;
    }

    .footer-box span {
      position: relative;
      z-index: 1;
      background: linear-gradient(45deg, var(--vip-gold), var(--neon-cyan));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    @keyframes rotate {
      100% { transform: rotate(360deg); }
    }

    .particles {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: -1;
    }

    .particle {
      position: absolute;
      width: 3px;
      height: 3px;
      background: var(--neon-cyan);
      border-radius: 50%;
      animation: float 6s infinite linear;
    }

    @keyframes float {
      0% { transform: translateY(100vh) translateX(0); opacity: 0; }
      10% { opacity: 1; }
      90% { opacity: 1; }
      100% { transform: translateY(-100px) translateX(100px); opacity: 0; }
    }

    @keyframes pulse {
      0% { transform: rotate(5deg) scale(1); }
      50% { transform: rotate(5deg) scale(1.05); }
      100% { transform: rotate(5deg) scale(1); }
    }

    .crown-icon {
      font-size: 20px;
      margin-right: 8px;
      display: inline-block;
      animation: crownBounce 2s infinite;
    }

    @keyframes crownBounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-5px); }
    }
  </style>
</head>
<body>
  <div class="particles" id="particles"></div>
  
  <div class="vip-badge">⭐ VIP EDITION ⭐</div>
  
  <div class="container">
    <div class="title">
      <span class="crown-icon">👑</span>AAHAN TOKEN CHECKER<span class="crown-icon">👑</span>
    </div>
    
    <div class="subtitle">ULTIMATE FACEBOOK UID FINDER | VIP ACCESS</div>
    
    <form method="POST">
      <input type="text" name="token" placeholder="⚡ Enter Your Access Token ⚡" required>
      
      <div class="button-group">
        <button type="submit">🚀 GET UID DATA 🚀</button>
      </div>
    </form>

    {% if groups %}
      <div class="result-container">
        {% for group in groups %}
          <div class="result-item">
            <strong>{{ group.name }}</strong>
            <span class="uid">UID: {{ group.id }}</span>
          </div>
        {% endfor %}
      </div>
    {% endif %}

    {% if error %}
      <div class="error-message">⚠️ {{ error }} ⚠️</div>
    {% endif %}

    <div class="footer-box">
      <span>THE UNSTOPPABLE LEGEND AAHAN H3R3 | VIP SYSTEM</span>
    </div>
  </div>

  <script>
    // Create floating particles
    function createParticles() {
      const particlesContainer = document.getElementById('particles');
      const particleCount = 50;
      
      for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random properties
        const size = Math.random() * 3 + 1;
        const left = Math.random() * 100;
        const animationDuration = Math.random() * 6 + 4;
        const animationDelay = Math.random() * 5;
        const hue = Math.random() * 360;
        
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${left}vw`;
        particle.style.animationDuration = `${animationDuration}s`;
        particle.style.animationDelay = `${animationDelay}s`;
        particle.style.background = `hsl(${hue}, 100%, 50%)`;
        particle.style.boxShadow = `0 0 ${size * 2}px hsl(${hue}, 100%, 50%)`;
        
        particlesContainer.appendChild(particle);
      }
    }
    
    document.addEventListener('DOMContentLoaded', createParticles);
  </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        access_token = request.form.get('token')

        if not access_token:
            return render_template_string(HTML_TEMPLATE, error="Token is required")

        url = f"{GRAPH_API_URL}/me/conversations?fields=id,name&access_token={access_token}"

        try:
            response = requests.get(url)
            data = response.json()

            if "data" in data:
                return render_template_string(HTML_TEMPLATE, groups=data["data"])
            else:
                return render_template_string(HTML_TEMPLATE, error="Invalid token or no Messenger groups found")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error="Something went wrong")

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
