/* Live prototype: a single phone whose tab content is rendered from JS
   so the whole flow is clickable end to end. */

(function () {
  "use strict";

  const body = document.getElementById("proto-body");
  if (!body) return;
  const nav = document.querySelector("#view-proto .nav");

  const state = { tab: "recap", voice: 0, playing: false };

  const MM = "class=\"mm\"";

  const SCREENS = {
    recap: () => `
      <div class="greeting">
        <div>
          <h2 class="mm">မင်္ဂလာပါ</h2>
          <div class="sub mm">၃ မိနစ် ရုပ်ရှင် ပြန်လည်ခြုံငုံမှု ဖန်တီးပါ</div>
        </div>
        <div class="avatar">◍</div>
      </div>
      <div class="orb-stage">
        <div class="orb" id="p-orb">
          <div class="ring"></div><div class="ring"></div><div class="ring"></div>
          <div class="spark"></div><div class="spark"></div>
          <div class="core"></div>
        </div>
        <div class="orb-caption"><div class="st mm" id="p-orbcap">3 မိနစ် ရုပ်ရှင် ပြန်လည်ခြုံငုံမှု ဖန်တီးပါ</div></div>
      </div>
      <div style="display:flex;justify-content:center">
        <button class="btn-primary" id="p-import">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M11 5h2v6h6v2h-6v6h-2v-6H5v-2h6z"/></svg>
          Import Movie
        </button>
      </div>
      <div class="hint"><button class="chip" id="p-think"><span class="d"></span>Simulate thinking</button></div>
      <div class="section-row"><h3 class="mm">မကြာမီ ဖန်တီးခဲ့သည်</h3><a href="#">အားလုံး</a></div>
      <div class="recents">
        <div class="recent"><div class="thumb"><span class="dur">02:58</span></div><div class="meta"><b class="mm">နွေဦးရာသီ</b><span>16:9 · ဒေသတွင်း</span></div></div>
        <div class="recent"><div class="thumb"><span class="dur">01:42</span></div><div class="meta"><b class="mm">တစ်ညအိပ်မက်</b><span>9:16 · ဒေသတွင်း</span></div></div>
      </div>`,

    editor: () => `
      <div class="section-row" style="margin-top:10px">
        <h2 style="font-family:var(--font-display);font-size:26px">တည်းဖြတ်</h2>
        <span class="chip">9:16 ⇄ 16:9</span>
      </div>
      <div class="editor-preview">
        <svg class="film" width="54" height="54" viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h16v16H4zm2 2v2h2V6zm10 0v2h2V6zM6 16v2h2v-2zm10 0v2h2v-2zM8 8h8v8H8z"/></svg>
        <div class="safe-grid"></div>
        <div class="overlay-box logo" data-x="34" data-y="30" style="transform:translate(34px,30px)">
          <span class="handle h1"></span><span class="handle h2"></span><span class="handle h3"></span><span class="handle h4"></span>LOGO
        </div>
        <div class="overlay-box sel" id="p-sub" data-x="30" data-y="210" style="transform:translate(30px,210px)">
          <span class="handle h1"></span><span class="handle h2"></span><span class="handle h3"></span><span class="handle h4"></span>
          ဇာတ်ကောင်က ခရီးစဉ်တစ်ခုကို စတင်ခဲ့သည်
        </div>
      </div>
      <div class="sheet">
        <div class="grab"></div>
        <div class="head"><h3 class="mm">စာသား ချိန်ညှိမှု</h3><span class="chip">16:9</span></div>
        <textarea class="textarea mm" rows="2">ဇာတ်ကောင်က ခရီးစဉ်တစ်ခုကို စတင်ခဲ့သည်</textarea>
        <div>
          <div class="field-label"><span>အရွယ်အစား</span><span class="val">15</span></div>
          <input class="slider" type="range" min="12" max="40" value="15" data-live-slider="#p-sub" />
        </div>
        <div class="swatches" data-target="#p-sub">
          <div class="swatch sel" data-color="#FFFFFF" style="background:#fff"></div>
          <div class="swatch" data-color="#F5C451" style="background:#F5C451"></div>
          <div class="swatch" data-color="#22D3EE" style="background:#22D3EE"></div>
          <div class="swatch" data-color="#7C5CFF" style="background:#7C5CFF"></div>
        </div>
      </div>`,

    voices: () => `
      <div style="padding-top:10px">
        <h2 class="mm" style="font-family:var(--font-mm);font-size:28px;font-weight:700">အသံ ရွေးချယ်မှု</h2>
        <div class="muted mm" style="font-size:13px;margin-top:4px">မြန်မာ အသံ ၅ မျိုးမှ ရွေးပါ</div>
      </div>
      <div class="voice-list" id="p-voices"></div>
      <div style="height:14px"></div>
      <button class="btn-primary" style="width:100%">ရွေးချယ်မည်</button>`,

    export: () => `
      <h2 style="font-family:var(--font-display);font-size:28px;padding-top:10px">ထုတ်ယူမှု</h2>
      <div style="height:14px"></div>
      <div class="card-pad">
        <div class="lbl">ကြည်လင်ပြတ်သားမှု</div>
        <div class="seg"><button aria-selected="false">720p</button><button aria-selected="true">1080p</button><button aria-selected="false">4K</button></div>
        <div class="lbl" style="margin-top:4px">ဖိုင်အမျိုးအစား</div>
        <div class="seg"><button aria-selected="true">MP4</button><button aria-selected="false">MOV</button></div>
      </div>
      <div class="card-pad">
        <div class="field-label"><span>အရည်အသွေး</span><span class="val">80%</span></div>
        <input class="slider" type="range" min="0" max="100" value="80" />
      </div>
      <div class="card-pad">
        <div class="progress-row">
          <div class="ring">
            <svg width="84" height="84">
              <defs><linearGradient id="pRing" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7C5CFF"/><stop offset="100%" stop-color="#22D3EE"/></linearGradient></defs>
              <circle class="track" cx="42" cy="42" r="37" fill="none" stroke-width="5"/>
              <circle class="bar" cx="42" cy="42" r="37" fill="none" stroke-width="5" stroke="url(#pRing)"/>
            </svg>
            <div class="thinking-border"></div>
            <div class="pct" id="p-pct">64%</div>
          </div>
          <div>
            <b style="font-size:14px" class="mm">ပြင်ဆင်နေသည်</b>
            <div class="muted mm" style="font-size:12px;margin:4px 0 8px">အသံနှင့် ဗီဒီယို ပေါင်းစပ်နေသည်…</div>
            <div style="display:flex;gap:6px"><span class="chip"><span class="d"></span>ffmpeg</span><span class="chip">edge-tts</span></div>
          </div>
        </div>
      </div>
      <button class="export-btn" id="p-export">
        <span class="bloom"></span>
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 3l7 7h-4v7h-6v-7H5z"/></svg>
        ထုတ်ယူမည်
      </button>`,
  };

  function render() {
    body.innerHTML = SCREENS[state.tab]();
    if (nav) {
      nav.querySelectorAll(".nav-item").forEach((n) =>
        n.setAttribute("aria-selected", String(n.dataset.tab === state.tab))
      );
    }
    wire();
  }

  function wire() {
    const t = state.tab;
    if (t === "recap") {
      const orb = body.querySelector("#p-orb");
      const cap = body.querySelector("#p-orbcap");
      body.querySelector("#p-think").addEventListener("click", () => {
        orb.classList.toggle("thinking");
        const on = orb.classList.contains("thinking");
        cap.textContent = on
          ? "AssemblyAI · စာသားထုတ်ယူနေသည်…"
          : "3 မိနစ် ရုပ်ရှင် ပြန်လည်ခြုံငုံမှု ဖန်တီးပါ";
      });
      body.querySelector("#p-import").addEventListener("click", () => {
        const scrim = document.createElement("div");
        scrim.className = "scrim";
        scrim.innerHTML = document.querySelector(".dialog") ? document.querySelector(".dialog").outerHTML : "";
        body.appendChild(scrim);
        scrim.querySelectorAll("[data-close-dialog]").forEach((b) =>
          b.addEventListener("click", () => scrim.remove())
        );
      });
    }
    if (t === "editor") {
      initDrag(body.querySelector(".editor-preview"));
      body.querySelectorAll("[data-live-slider]").forEach((s) => {
        const out = s.parentElement.parentElement.querySelector(".val");
        s.addEventListener("input", () => {
          if (out) out.textContent = s.value;
          const tgt = body.querySelector(s.dataset.liveSlider);
          if (tgt) tgt.style.fontSize = s.value + "px";
        });
      });
      body.querySelectorAll(".swatches").forEach((row) => {
        row.querySelectorAll(".swatch").forEach((sw) =>
          sw.addEventListener("click", () => {
            row.querySelectorAll(".swatch").forEach((x) => x.classList.remove("sel"));
            sw.classList.add("sel");
            const tgt = body.querySelector(row.dataset.target);
            if (tgt) tgt.style.color = sw.dataset.color;
          })
        );
      });
    }
    if (t === "voices") {
      renderVoices();
    }
    if (t === "export") {
      body.querySelectorAll(".seg").forEach((seg) =>
        seg.querySelectorAll("button").forEach((b) =>
          b.addEventListener("click", () => {
            seg.querySelectorAll("button").forEach((x) => x.setAttribute("aria-selected", "false"));
            b.setAttribute("aria-selected", "true");
          })
        )
      );
      body.querySelector("#p-export").addEventListener("click", () => {
        const bloom = body.querySelector(".bloom");
        bloom.classList.remove("go");
        void bloom.offsetWidth;
        bloom.classList.add("go");
        const pct = body.querySelector("#p-pct");
        let p = 0;
        const id = setInterval(() => {
          p = Math.min(100, p + 9);
          pct.textContent = p + "%";
          if (p >= 100) { clearInterval(id); pct.textContent = "✓"; }
        }, 80);
      });
    }
  }

  function renderVoices() {
    const host = body.querySelector("#p-voices");
    const labels = [
      "မြန်မာ အမျိုးသမီး ၁", "မြန်မာ အမျိုးသမီး ၂",
      "မြန်မာ အမျိုးသား ၁", "မြန်မာ အမျိုးသား ၂", "မြန်မာ အမျိုးသား ၃",
    ];
    host.innerHTML = labels.map((label, i) => {
      const bars = Array.from({ length: 20 }, (_, b) =>
        '<span style="animation-delay:' + (b * 0.05).toFixed(2) + 's"></span>'
      ).join("");
      return `
        <div class="voice-card ${i === state.voice ? "sel" : ""}" data-i="${i}">
          <div class="badge"><svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M12 14a3 3 0 003-3V5a3 3 0 00-6 0v6a3 3 0 003 3zm5-3a5 5 0 01-10 0H5a7 7 0 006 6.92V21h2v-3.08A7 7 0 0019 11z"/></svg></div>
          <div class="info"><b class="mm">${label}</b><div class="wave">${bars}</div></div>
          <button class="playbtn" data-play="${i}">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
          </button>
        </div>`;
    }).join("");

    host.querySelectorAll(".voice-card").forEach((card) =>
      card.addEventListener("click", () => {
        state.voice = Number(card.dataset.i);
        host.querySelectorAll(".voice-card").forEach((c) => c.classList.remove("sel"));
        card.classList.add("sel");
      })
    );
    host.querySelectorAll("[data-play]").forEach((btn) =>
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const card = btn.closest(".voice-card");
        const wave = card.querySelector(".wave");
        const on = !btn.classList.contains("on");
        btn.classList.toggle("on", on);
        wave.classList.toggle("on", on);
        btn.innerHTML = on
          ? '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>'
          : '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
        if (on) {
          setTimeout(() => {
            btn.classList.remove("on");
            wave.classList.remove("on");
            btn.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
          }, 3200);
        }
      })
    );
  }

  /* drag-to-place with magnetic snapping, shared with the board screens */
  function initDrag(stage) {
    if (!stage) return;
    const grid = stage.querySelector(".safe-grid");
    const boxes = stage.querySelectorAll(".overlay-box");
    boxes.forEach((box) => {
      box.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        boxes.forEach((b) => b.classList.remove("sel"));
        box.classList.add("sel");
        grid && grid.classList.add("show");
        box.setPointerCapture(e.pointerId);
        const rect = stage.getBoundingClientRect();
        const sx = e.clientX, sy = e.clientY;
        const bx = parseFloat(box.dataset.x || "0");
        const by = parseFloat(box.dataset.y || "0");
        function move(ev) {
          let nx = bx + (ev.clientX - sx);
          let ny = by + (ev.clientY - sy);
          const snap = (v, targets, th = 8) => {
            for (const tt of targets) if (Math.abs(v - tt) < th) return tt;
            return v;
          };
          nx = snap(nx, [rect.width * 0.5 - box.offsetWidth / 2, 12, rect.width - box.offsetWidth - 12]);
          ny = snap(ny, [12, rect.height * 0.5 - box.offsetHeight / 2, rect.height - box.offsetHeight - 12]);
          box.dataset.x = String(nx);
          box.dataset.y = String(ny);
          box.style.transform = `translate(${nx}px, ${ny}px)`;
        }
        function up(ev) {
          box.removeEventListener("pointermove", move);
          box.removeEventListener("pointerup", up);
          try { box.releasePointerCapture(ev.pointerId); } catch (_) {}
          setTimeout(() => grid && grid.classList.remove("show"), 800);
        }
        box.addEventListener("pointermove", move);
        box.addEventListener("pointerup", up);
      });
    });
  }

  if (nav) {
    nav.querySelectorAll(".nav-item").forEach((n) =>
      n.addEventListener("click", () => {
        state.tab = n.dataset.tab;
        render();
      })
    );
  }

  render();
})();
