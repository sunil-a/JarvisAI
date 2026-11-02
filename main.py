import datetime
import subprocess
import webbrowser
from urllib.parse import quote

import pyttsx3
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

engine = pyttsx3.init()
engine.setProperty("rate", 175)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JARVIS AI</title>
<style>
* { box-sizing: border-box; }
body {
  margin: 0; min-height: 100vh; display: grid; place-items: center;
  background: radial-gradient(circle, #10243b, #03070e 75%);
  color: #00eaff; font-family: Arial, sans-serif;
}
main { width: min(600px, 94%); text-align: center; padding: 24px; }
h1 { letter-spacing: 8px; text-shadow: 0 0 18px #00eaff; }
.robot {
  width: 190px; height: 160px; margin: 35px auto;
  border: 3px solid #00eaff; border-radius: 45%;
  background: linear-gradient(145deg, #29465d, #09121e);
  box-shadow: 0 0 35px #007e99;
  display: grid; place-items: center;
}
.eyes { display: flex; gap: 30px; }
.eye {
  width: 36px; height: 22px; background: #00eaff;
  border-radius: 50%; box-shadow: 0 0 20px #00eaff;
}
.mouth { width: 55px; height: 7px; background: #00eaff; }
.panel {
  padding: 20px; border: 1px solid #007e99;
  border-radius: 15px; background: #071625;
}
input {
  width: 100%; padding: 13px; margin: 12px 0;
  border: 1px solid #00eaff; border-radius: 8px;
  background: #03070e; color: white;
}
button {
  padding: 12px 16px; margin: 5px; border-radius: 25px;
  border: 1px solid #00eaff; background: transparent;
  color: #00eaff; cursor: pointer;
}
button:hover { background: #00eaff; color: #03070e; }
#status { min-height: 25px; color: #c4e9ff; }
small { color: #8caec7; }
</style>
</head>
<body>
<main>
  <h1>J.A.R.V.I.S</h1>
  <small>PERSONAL DESKTOP ASSISTANT</small>

  <div class="robot">
    <div>
      <div class="eyes"><div class="eye"></div><div class="eye"></div></div>
      <div class="mouth" style="margin:25px auto 0"></div>
    </div>
  </div>

  <section class="panel">
    <p id="status">Jarvis is ready. Enter a command.</p>
    <input id="command" placeholder="Try: open YouTube or what time is it">
    <button onclick="sendCommand()">RUN COMMAND</button>
    <button onclick="startVoice()">🎤 VOICE INPUT</button>
    <br>
    <small>Commands run on your computer. Confirm sensitive actions yourself.</small>
  </section>
</main>

<script>
async function sendCommand(text) {
  const input = document.getElementById("command");
  const command = text || input.value;
  if (!command.trim()) return;

  document.getElementById("status").textContent = "Processing...";
  try {
    const response = await fetch("/command", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({command})
    });
    const data = await response.json();
    document.getElementById("status").textContent = data.message;
    if (!text) input.value = "";
  } catch {
    document.getElementById("status").textContent =
      "Could not connect to Jarvis.";
  }
}

function startVoice() {
  const Recognition = window.SpeechRecognition ||
                      window.webkitSpeechRecognition;

  if (!Recognition) {
    document.getElementById("status").textContent =
      "Voice recognition is unavailable in this browser. Type a command.";
    return;
  }

  const recognition = new Recognition();
  recognition.lang = "en-US";
  recognition.onstart = () =>
    document.getElementById("status").textContent = "Listening...";
  recognition.onresult = event =>
    sendCommand(event.results[0][0].transcript);
  recognition.onerror = () =>
    document.getElementById("status").textContent =
      "Voice recognition failed. Try typing a command.";
  recognition.start();
}

document.getElementById("command").addEventListener("keydown", e => {
  if (e.key === "Enter") sendCommand();
});
</script>
</body>
</html>
"""


def speak(message):
    """Speak a response using the computer's local speech engine."""
    try:
        engine.say(message)
        engine.runAndWait()
    except Exception:
        pass


def process_command(command):
    command = command.lower().strip()

    if "time" in command:
        return "The time is " + datetime.datetime.now().strftime("%I:%M %p")

    if "date" in command:
        return "Today is " + datetime.datetime.now().strftime("%d %B %Y")

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    if "open calculator" in command:
        subprocess.Popen("calc.exe")
        return "Opening Calculator."

    if "open notepad" in command:
        subprocess.Popen("notepad.exe")
        return "Opening Notepad."

    if command.startswith("search for "):
        query = command.removeprefix("search for ").strip()
        if query:
            webbrowser.open(
                "https://www.google.com/search?q=" + quote(query)
            )
            return "Searching Google for " + query

    if command in {"hello", "hello jarvis", "hi jarvis"}:
        return "Hello! Jarvis is ready."

    return (
        "I don't know that command yet. "
        "Try open YouTube, open Calculator, or what time is it."
    )


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}
    user_command = data.get("command", "")

    if not isinstance(user_command, str) or not user_command.strip():
        return jsonify(message="Please enter a command."), 400

    message = process_command(user_command)
    speak(message)
    return jsonify(message=message)


if __name__ == "__main__":
    print("JARVIS is starting...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(host="127.0.0.1", port=5000, debug=False)