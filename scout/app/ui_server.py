from __future__ import annotations

import json
from dataclasses import dataclass, field
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


@dataclass(slots=True)
class RobotUIState:
    name: str = "SCOUT"
    mode: str = "development"
    ready: bool = True
    status: str = "Online and listening"
    greeting: str = "Hello, I can see you, hear you, and talk with you."
    capabilities: list[str] = field(
        default_factory=lambda: [
            "camera",
            "microphone",
            "speech",
            "vision",
            "memory",
            "local-ai",
        ]
    )
    face_states: list[str] = field(
        default_factory=lambda: [
            "idle",
            "listening",
            "thinking",
            "speaking",
            "happy",
            "confused",
            "surprised",
            "sleeping",
        ]
    )
    summary: str = "Local-first companion robot for live perception and voice interaction."


def build_robot_ui_state(mode: str = "development", ready: bool = True) -> RobotUIState:
    return RobotUIState(
        mode=mode,
        ready=ready,
        status="Ready for conversation" if ready else "Starting up",
        greeting="Hello, I can see you, hear you, and talk with you.",
    )


def render_robot_ui_html(state: RobotUIState) -> str:
    return f"""<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{escape(state.name)} Robot UI</title>
    <style>
      :root {{
        --bg-1: #07111f;
        --bg-2: #111f34;
        --panel: rgba(17, 26, 44, 0.82);
        --panel-strong: rgba(10, 19, 33, 0.95);
        --line: rgba(133, 204, 255, 0.28);
        --text: #edf6ff;
        --muted: #9ab7d6;
        --cyan: #67d5ff;
        --blue: #4f8cff;
        --green: #59f0a8;
        --amber: #ffca6e;
        --red: #ff7d7d;
      }}

      * {{ box-sizing: border-box; }}

      body {{
        margin: 0;
        min-height: 100vh;
        font-family: Arial, Helvetica, sans-serif;
        color: var(--text);
        background: radial-gradient(circle at top, var(--bg-2), var(--bg-1) 58%);
      }}

      .app-shell {{
        width: min(1400px, calc(100vw - 32px));
        margin: 24px auto;
        display: grid;
        grid-template-columns: 300px minmax(0, 1fr) 320px;
        gap: 20px;
      }}

      .panel {{
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 22px;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
      }}

      .left-panel, .right-panel {{
        padding: 20px;
      }}

      .brand {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 18px;
      }}

      .logo {{
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: linear-gradient(135deg, var(--cyan), var(--blue));
        box-shadow: 0 12px 28px rgba(79, 140, 255, 0.48);
        position: relative;
      }}

      .logo::before, .logo::after {{
        content: "";
        position: absolute;
        background: white;
        border-radius: 50%;
        top: 12px;
      }}

      .logo::before {{ width: 7px; height: 7px; left: 12px; }}
      .logo::after {{ width: 7px; height: 7px; right: 12px; }}

      h1 {{
        margin: 0;
        font-size: 1.7rem;
      }}

      .status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(89, 240, 168, 0.14);
        border: 1px solid rgba(89, 240, 168, 0.38);
        color: var(--green);
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }}

      .status-dot {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 12px var(--green);
      }}

      .story {{
        margin-top: 18px;
        color: var(--muted);
        line-height: 1.5;
      }}

      .section-title {{
        margin: 24px 0 14px;
        color: var(--muted);
        font-size: 0.76rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }}

      .capability-list {{
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 10px;
      }}

      .capability-list li {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(136, 190, 255, 0.06);
        border: 1px solid rgba(136, 190, 255, 0.15);
      }}

      .capability-list span:first-child {{
        text-transform: capitalize;
      }}

      .pill {{
        min-width: 78px;
        text-align: center;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(103, 213, 255, 0.12);
        color: var(--cyan);
        font-size: 0.72rem;
        font-weight: 700;
      }}

      .middle-panel {{
        padding: 20px;
      }}

      .robot-badge {{
        display: inline-flex;
        align-items: center;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(103, 213, 255, 0.1);
        border: 1px solid rgba(103, 213, 255, 0.22);
        color: var(--cyan);
        font-size: 0.76rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}

      .top-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 18px;
        margin-bottom: 18px;
      }}

      .robot-indicator {{
        color: var(--muted);
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}

      .face-shell {{
        background: linear-gradient(180deg, rgba(17, 26, 44, 0.94), rgba(8, 14, 23, 0.96));
        border: 1px solid rgba(133, 204, 255, 0.2);
        border-radius: 26px;
        padding: 22px;
      }}

      .robot-face {{
        width: min(100%, 520px);
        aspect-ratio: 1.18;
        margin: 0 auto;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 30px;
        background: radial-gradient(circle at top, rgba(103, 213, 255, 0.16), rgba(12, 17, 28, 0.9));
      }}

      .head {{
        width: 240px;
        height: 240px;
        background: linear-gradient(180deg, #f5f9ff, #dfeeff 58%, #bcd0ef 100%);
        border: 3px solid rgba(92, 126, 165, 0.8);
        border-radius: 48% 48% 42% 42%;
        box-shadow: inset 0 -10px 24px rgba(77, 98, 134, 0.18), 0 18px 34px rgba(11, 22, 34, 0.45);
        position: relative;
      }}

      .ear {{
        position: absolute;
        width: 26px;
        height: 56px;
        background: #dfeeff;
        border: 3px solid rgba(92, 126, 165, 0.8);
        border-radius: 18px;
        top: 78px;
      }}

      .ear.left {{ left: -18px; }}
      .ear.right {{ right: -18px; }}

      .eye-pair {{
        position: absolute;
        left: 50%;
        top: 84px;
        transform: translateX(-50%);
        display: flex;
        gap: 28px;
      }}

      .eye {{
        width: 38px;
        height: 44px;
        background: #1f2f45;
        border-radius: 50% 50% 46% 46%;
        position: relative;
      }}

      .eye::after {{
        content: "";
        position: absolute;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: white;
        top: 8px;
        left: 9px;
      }}

      .mouth {{
        position: absolute;
        left: 50%;
        top: 154px;
        transform: translateX(-50%);
        width: 92px;
        height: 42px;
        border-bottom: 7px solid #2a4367;
        border-radius: 0 0 80px 80px;
      }}

      .antenna {{
        position: absolute;
        left: 50%;
        top: -26px;
        transform: translateX(-50%);
        width: 8px;
        height: 38px;
        background: rgba(116, 144, 176, 0.85);
        border-radius: 10px;
      }}

      .antenna::before {{
        content: "";
        position: absolute;
        width: 20px;
        height: 20px;
        background: var(--amber);
        border-radius: 50%;
        top: -18px;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0 0 14px rgba(255, 202, 110, 0.8);
      }}

      .robot-face[data-state="listening"] .eye {{
        height: 18px;
        transform: scaleY(0.8);
      }}

      .robot-face[data-state="thinking"] .eye {{
        width: 48px;
        border-radius: 35%;
      }}

      .robot-face[data-state="speaking"] .mouth {{
        width: 112px;
        height: 58px;
        border-bottom-width: 10px;
        animation: talk 0.5s ease-in-out infinite alternate;
      }}

      .robot-face[data-state="happy"] .mouth {{
        width: 108px;
        height: 60px;
        border-bottom: 0;
        border-top: 7px solid #2a4367;
        border-radius: 80px 80px 0 0;
        top: 160px;
      }}

      .robot-face[data-state="confused"] .eye {{
        border-radius: 30% 30% 50% 50%;
      }}

      .robot-face[data-state="surprised"] .mouth {{
        width: 78px;
        height: 78px;
        border: 7px solid #2a4367;
        border-radius: 50%;
      }}

      .robot-face[data-state="sleeping"] .eye {{
        height: 7px;
        border-radius: 999px;
      }}

      .robot-face[data-state="error"] .mouth {{
        border-bottom: 7px solid var(--red);
      }}

      @keyframes talk {{
        from {{ transform: translateX(-50%) scaleY(0.9); }}
        to {{ transform: translateX(-50%) scaleY(1.25); }}
      }}

      .controls {{
        display: flex;
        gap: 12px;
        justify-content: center;
        margin-top: 18px;
        flex-wrap: wrap;
      }}

      button {{
        border: none;
        border-radius: 14px;
        padding: 12px 18px;
        cursor: pointer;
        font-size: 0.95rem;
        font-weight: 700;
        transition: transform 0.18s ease, opacity 0.18s ease;
      }}

      button:hover {{ transform: translateY(-1px); }}
      button:active {{ transform: translateY(1px); }}

      .primary {{
        background: linear-gradient(135deg, var(--cyan), var(--blue));
        color: white;
      }}

      .secondary {{
        background: rgba(103, 213, 255, 0.1);
        color: var(--text);
        border: 1px solid rgba(103, 213, 255, 0.22);
      }}

      .live-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 16px;
      }}

      .stream-card {{
        background: rgba(8, 15, 23, 0.76);
        border: 1px solid rgba(133, 204, 255, 0.22);
        border-radius: 18px;
        overflow: hidden;
      }}

      .video-frame {{
        width: 100%;
        height: 210px;
        background: linear-gradient(180deg, #0d1b2d, #07111f);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--muted);
      }}

      video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        background: #020a12;
      }}

      .stream-label {{
        padding: 12px 14px;
        font-size: 0.82rem;
        color: var(--muted);
        border-top: 1px solid rgba(133, 204, 255, 0.12);
      }}

      .log-box {{
        margin-top: 16px;
        padding: 14px;
        height: 180px;
        overflow: auto;
        border-radius: 16px;
        background: rgba(8, 15, 23, 0.82);
        border: 1px solid rgba(133, 204, 255, 0.18);
      }}

      .log-item {{
        margin-bottom: 10px;
        line-height: 1.45;
        color: var(--muted);
      }}

      .log-item strong {{ color: var(--text); }}

      .stats-grid {{
        display: grid;
        gap: 12px;
      }}

      .stat-card {{
        padding: 14px;
        border-radius: 14px;
        background: rgba(136, 190, 255, 0.05);
        border: 1px solid rgba(136, 190, 255, 0.12);
      }}

      .stat-value {{
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 8px;
      }}

      .muted {{ color: var(--muted); }}

      @media (max-width: 980px) {{
        .app-shell {{
          grid-template-columns: 1fr;
        }}

        .live-grid {{
          grid-template-columns: 1fr;
        }}
      }}
    </style>
  </head>
  <body>
    <div class=\"app-shell\">
      <aside class=\"panel left-panel\">
        <div class=\"brand\">
          <div class=\"logo\"></div>
          <div>
            <h1>{escape(state.name)}</h1>
          </div>
        </div>

        <div class=\"status-pill\"><span class=\"status-dot\"></span> {escape(state.status)}</div>

        <p class=\"story\">{escape(state.summary)}</p>

        <div class=\"section-title\">Capabilities</div>
        <ul class=\"capability-list\">
          {''.join(f'<li><span>{escape(item.title())}</span><span class="pill">live</span></li>' for item in state.capabilities)}
        </ul>
      </aside>

      <main class=\"panel middle-panel\">
        <div class=\"top-row\">
            <div class=\"robot-badge\">robot mode · {escape(state.mode)}</div>
        </div>

        <div class=\"face-shell\">
          <div class=\"robot-face\" id=\"robotFace\" data-state=\"idle\">
            <div class=\"antenna\"></div>
            <div class=\"ear left\"></div>
            <div class=\"ear right\"></div>
            <div class=\"head\">
              <div class=\"eye-pair\">
                <div class=\"eye\"></div>
                <div class=\"eye\"></div>
              </div>
              <div class=\"mouth\"></div>
            </div>
          </div>

          <div class=\"controls\">
            <button id=\"listenButton\" class=\"primary\">Listen</button>
            <button id=\"speakButton\" class=\"secondary\">Speak</button>
            <button id=\"idleButton\" class=\"secondary\">Idle</button>
          </div>
        </div>

        <div class=\"live-grid\">
          <div class=\"stream-card\">
            <div class=\"video-frame\">
              <video id=\"cameraPreview\" autoplay playsinline muted></video>
            </div>
            <div class=\"stream-label\" id=\"cameraStatus\">Camera is waiting for permission.</div>
          </div>

          <div class=\"stream-card\">
            <div class=\"video-frame\" style=\"display: flex; align-items: center; justify-content: center;\">
              <div id=\"audioWave\" style=\"font-size: 32px; letter-spacing: 6px; color: var(--cyan);\">▁▂▃▄▅▆▇</div>
            </div>
            <div class=\"stream-label\" id=\"audioStatus\">Microphone standby.</div>
          </div>
        </div>

        <div class=\"log-box\" id=\"speechLog\">
          <div class=\"log-item\"><strong>SCOUT:</strong> {escape(state.greeting)}</div>
        </div>
      </main>

      <aside class=\"panel right-panel\">
        <div class=\"section-title\">System</div>
        <div class=\"stats-grid\">
          <div class=\"stat-card\">
            <div class=\"muted\">Face state</div>
            <div class=\"stat-value\" id=\"stateValue\">idle</div>
          </div>
          <div class=\"stat-card\">
            <div class=\"muted\">Speech</div>
            <div class=\"stat-value\" id=\"speechValue\">ready</div>
          </div>
          <div class=\"stat-card\">
            <div class=\"muted\">Camera</div>
            <div class=\"stat-value\" id=\"cameraValue\">offline</div>
          </div>
          <div class=\"stat-card\">
            <div class=\"muted\">Audio</div>
            <div class=\"stat-value\" id=\"audioValue\">standby</div>
          </div>
        </div>
      </aside>
    </div>

    <script>
      const face = document.getElementById('robotFace');
      const stateValue = document.getElementById('stateValue');
      const speechValue = document.getElementById('speechValue');
      const cameraValue = document.getElementById('cameraValue');
      const audioValue = document.getElementById('audioValue');
      const speechLog = document.getElementById('speechLog');
      const cameraPreview = document.getElementById('cameraPreview');
      const cameraStatus = document.getElementById('cameraStatus');
      const audioStatus = document.getElementById('audioStatus');

      function setFaceState(nextState) {{
        face.dataset.state = nextState;
        stateValue.textContent = nextState;
      }}

      function appendLog(role, message) {{
        const item = document.createElement('div');
        item.className = 'log-item';
        item.innerHTML = '<strong>' + role + ':</strong> ' + message;
        speechLog.prepend(item);
      }}

      async function enableCamera() {{
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {{
          cameraStatus.textContent = 'Camera access is not supported in this browser.';
          return;
        }}

        try {{
          const stream = await navigator.mediaDevices.getUserMedia({{ video: true, audio: false }});
          cameraPreview.srcObject = stream;
          cameraStatus.textContent = 'Camera live: your face is visible to SCOUT.';
          cameraValue.textContent = 'live';
          setFaceState('listening');
        }} catch (error) {{
          cameraStatus.textContent = 'Camera permission was blocked.';
          cameraValue.textContent = 'blocked';
        }}
      }}

      async function enableMicrophone() {{
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {{
          audioStatus.textContent = 'Microphone is unavailable in this browser.';
          return;
        }}

        try {{
          const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
          const audioContext = new (window.AudioContext || window.webkitAudioContext)();
          const analyser = audioContext.createAnalyser();
          const source = audioContext.createMediaStreamSource(stream);
          source.connect(analyser);
          analyser.fftSize = 256;
          const data = new Uint8Array(analyser.frequencyBinCount);

          function drawWave() {{
            analyser.getByteFrequencyData(data);
            const average = data.reduce((sum, value) => sum + value, 0) / data.length;
            const bars = '▁▂▃▄▅▆▇';
            const index = Math.min(bars.length - 1, Math.max(0, Math.floor(average / 32)));
            audioStatus.textContent = 'Microphone live: hearing your voice.';
            audioValue.textContent = 'live';
            document.getElementById('audioWave').textContent = bars.slice(0, index + 1) || '▁';
            requestAnimationFrame(drawWave);
          }}

          drawWave();
          setFaceState('listening');
        }} catch (error) {{
          audioStatus.textContent = 'Microphone permission was blocked.';
          audioValue.textContent = 'blocked';
        }}
      }}

      function speakText(text) {{
        if ('speechSynthesis' in window) {{
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.rate = 1.0;
          utterance.pitch = 1.1;
          utterance.volume = 1.0;
          speechValue.textContent = 'speaking';
          setFaceState('speaking');
          appendLog('SCOUT', text);
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(utterance);
          utterance.onend = () => {{
            setFaceState('idle');
            speechValue.textContent = 'ready';
          }};
        }} else {{
          appendLog('SCOUT', text);
          setFaceState('happy');
        }}
      }}

      function startVoiceInput() {{
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {{
          appendLog('SCOUT', 'Speech recognition is not available in this browser. Grant mic access or use a browser with Web Speech enabled.');
          return;
        }}

        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {{
          setFaceState('listening');
          speechValue.textContent = 'listening';
          appendLog('YOU', 'Listening...');
        }};

        recognition.onresult = (event) => {{
          const transcript = event.results[0][0].transcript;
          appendLog('YOU', transcript);
          setFaceState('thinking');
          speechValue.textContent = 'thinking';

          const robotReply = transcript.toLowerCase().includes('hello')
            ? 'Hello. I can see your face and hear your voice. I am ready to help.'
            : 'I hear you. I am SCOUT, and I am ready to support you with my face, voice, and local intelligence.';

          speakText(robotReply);
        }};

        recognition.onerror = () => {{
          appendLog('SCOUT', 'I could not interpret that audio. Please try again.');
          setFaceState('confused');
          speechValue.textContent = 'ready';
        }};

        recognition.onend = () => {{
          setFaceState('idle');
          speechValue.textContent = 'ready';
        }};

        recognition.start();
      }}

      document.getElementById('listenButton').addEventListener('click', () => {{
        enableCamera();
        enableMicrophone();
        startVoiceInput();
      }});

      document.getElementById('speakButton').addEventListener('click', () => {{
        speakText('Hello. I can see your face and hear your voice. How can I help today?');
      }});

      document.getElementById('idleButton').addEventListener('click', () => {{
        setFaceState('idle');
        speechValue.textContent = 'ready';
      }});

      enableCamera();
      enableMicrophone();
      setFaceState('idle');
    </script>
  </body>
</html>
"""


class RobotUIRequestHandler(BaseHTTPRequestHandler):
    server_version = "SCOUT/1.0"

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path in {"/", "/index.html"}:
            payload = render_robot_ui_html(self.server.ui_state).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        if self.path == "/api/status":
            data = json.dumps({
                "name": self.server.ui_state.name,
                "mode": self.server.ui_state.mode,
                "ready": self.server.ui_state.ready,
                "status": self.server.ui_state.status,
                "capabilities": self.server.ui_state.capabilities,
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003 - interface override
        return


def start_robot_ui(host: str = "0.0.0.0", port: int = 8000, state: RobotUIState | None = None) -> ThreadingHTTPServer:
    ui_state = state or build_robot_ui_state()
    chosen_port = port
    last_error: OSError | None = None

    while True:
        try:
            server = ThreadingHTTPServer((host, chosen_port), RobotUIRequestHandler)
            break
        except OSError as exc:
            if chosen_port == 0:
                raise
            last_error = exc
            chosen_port = chosen_port + 1
            if chosen_port > 65535:
                raise last_error

    server.ui_state = ui_state
    if chosen_port != port:
        print(f"Port {port} is busy; SCOUT UI started on http://localhost:{chosen_port}")
    return server


def main() -> int:
    server = start_robot_ui(host="0.0.0.0", port=8000)
    print(f"SCOUT UI ready at http://localhost:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
