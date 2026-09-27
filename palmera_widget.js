/**
 * Palmera Travel & Services - AI Chatbot Widget
 * Embeddable Widget for Palmera Travel Website
 * Author: Montassar Chorfi
 */

(function () {
    // Configuration
    const API_BASE_URL = "http://localhost:8000/api/v1"; // Replace with your production API URL
    const WHATSAPP_NUMBER = "21653244178";
    const SESSION_ID = "palmera_" + Math.random().toString(36).substring(2, 9);

    // CSS Styles Injection
    const style = document.createElement('style');
    style.innerHTML = `
        .palmera-chat-widget-btn {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: linear-gradient(135deg, #d4a843, #8B4513);
            color: #ffffff;
            border: none;
            border-radius: 50px;
            padding: 14px 22px;
            font-family: 'Cairo', 'Tajawal', sans-serif;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            z-index: 99999;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
        }
        .palmera-chat-widget-btn:hover {
            transform: translateY(-4px) scale(1.03);
            box-shadow: 0 14px 30px rgba(0, 0, 0, 0.4);
        }
        .palmera-chat-modal {
            display: none;
            position: fixed;
            bottom: 90px;
            right: 25px;
            width: 380px;
            max-width: 90vw;
            height: 520px;
            max-height: 80vh;
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.25);
            z-index: 99999;
            flex-direction: column;
            overflow: hidden;
            font-family: 'Cairo', 'Tajawal', sans-serif;
            border: 1px solid rgba(212, 168, 67, 0.3);
        }
        .palmera-chat-header {
            background: linear-gradient(135deg, #2c1810, #8B4513);
            color: #ffffff;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .palmera-chat-header h4 {
            margin: 0;
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .palmera-chat-close {
            background: none;
            border: none;
            color: #ffffff;
            font-size: 20px;
            cursor: pointer;
        }
        .palmera-chat-body {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #fdfbf7;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .palmera-msg {
            max-width: 85%;
            padding: 12px 16px;
            border-radius: 16px;
            font-size: 14px;
            line-height: 1.5;
        }
        .palmera-msg-user {
            align-self: flex-end;
            background: #8B4513;
            color: #ffffff;
            border-bottom-left-radius: 4px;
        }
        .palmera-msg-bot {
            align-self: flex-start;
            background: #ffffff;
            color: #2c1810;
            border: 1px solid #e2d8c3;
            border-bottom-right-radius: 4px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .palmera-whatsapp-btn {
            display: inline-block;
            margin-top: 10px;
            background: #25d366;
            color: #ffffff;
            padding: 8px 14px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 12px;
            font-weight: 700;
        }
        .palmera-chat-footer {
            padding: 12px;
            background: #ffffff;
            border-top: 1px solid #eee;
            display: flex;
            gap: 8px;
        }
        .palmera-chat-input {
            flex: 1;
            padding: 10px 14px;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-family: inherit;
            font-size: 14px;
            outline: none;
        }
        .palmera-chat-send {
            background: #8B4513;
            color: #fff;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            font-size: 16px;
        }
    `;
    document.head.appendChild(style);

    // Create Elements
    const widgetBtn = document.createElement('button');
    widgetBtn.className = 'palmera-chat-widget-btn';
    widgetBtn.innerHTML = '🤖 <span>المساعد السياحي الذكي</span>';

    const modal = document.createElement('div');
    modal.className = 'palmera-chat-modal';
    modal.innerHTML = `
        <div class="palmera-chat-header">
            <h4>🌴 Palmera Travel Assistant</h4>
            <button class="palmera-chat-close" id="palmeraClose">&times;</button>
        </div>
        <div class="palmera-chat-body" id="palmeraBody">
            <div class="palmera-msg palmera-msg-bot">
                مرحباً بك في <b>Palmera Travel & Services</b>! 🌴<br>
                أنا مساعدك السياحي الذكي. كيف يمكنني مساعدتك في تخطيط رحلتك أو حجز الفنادق والتذاكر في تونس اليوم؟
            </div>
        </div>
        <div class="palmera-chat-footer">
            <input type="text" class="palmera-chat-input" id="palmeraInput" placeholder="اسأل عن الرحلات أو الفنادق..." dir="rtl">
            <button class="palmera-chat-send" id="palmeraSend">➤</button>
        </div>
    `;

    document.body.appendChild(widgetBtn);
    document.body.appendChild(modal);

    // Toggle Modal
    widgetBtn.onclick = () => {
        modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
    };
    document.getElementById('palmeraClose').onclick = () => {
        modal.style.display = 'none';
    };

    // Send Message Logic
    async function sendMessage() {
        const input = document.getElementById('palmeraInput');
        const body = document.getElementById('palmeraBody');
        const question = input.value.trim();
        if (!question) return;

        // User Message
        const userMsg = document.createElement('div');
        userMsg.className = 'palmera-msg palmera-msg-user';
        userMsg.innerText = question;
        body.appendChild(userMsg);

        input.value = '';
        body.scrollTop = body.scrollHeight;

        // Loading Indicator
        const loadingMsg = document.createElement('div');
        loadingMsg.className = 'palmera-msg palmera-msg-bot';
        loadingMsg.innerText = '⏳ جاري البحث في العروض والإجابة...';
        body.appendChild(loadingMsg);
        body.scrollTop = body.scrollHeight;

        try {
            const resp = await fetch(`${API_BASE_URL}/query?question=${encodeURIComponent(question)}&session_id=${SESSION_ID}`, {
                method: 'POST'
            });
            const data = await resp.json();
            body.removeChild(loadingMsg);

            const botMsg = document.createElement('div');
            botMsg.className = 'palmera-msg palmera-msg-bot';
            let text = data.answer || "عذراً، لم أستطع الإجابة حالياً.";
            
            // Add WhatsApp Action Button
            const waUrl = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent("مرحباً Palmera Travel، أود الاستفسار والحجز بناءً على المحادثة: " + question)}`;
            text += `<br><a href="${waUrl}" target="_blank" class="palmera-whatsapp-btn">💬 تواصل واحجز فوراً عبر WhatsApp</a>`;

            botMsg.innerHTML = text;
            body.appendChild(botMsg);
            body.scrollTop = body.scrollHeight;
        } catch (err) {
            body.removeChild(loadingMsg);
            const errMsg = document.createElement('div');
            errMsg.className = 'palmera-msg palmera-msg-bot';
            errMsg.innerText = '❌ تعذر الاتصال بخادم الخدمة. يرجى محاولة التواصل عبر الهاتف +216 53 244 178.';
            body.appendChild(errMsg);
        }
    }

    document.getElementById('palmeraSend').onclick = sendMessage;
    document.getElementById('palmeraInput').onkeypress = (e) => {
        if (e.key === 'Enter') sendMessage();
    };
})();
