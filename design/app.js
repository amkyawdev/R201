/* Movie Recap Myanmar — prototype interactions.
   Kept dependency-free so the board opens straight from the file system. */

(function () {
  "use strict";

  /* ---------------------------------------------------- icon set */
  const ICON = {
    play: '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
    pause: '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>',
    recap: { out: "M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V4z", fill: "M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V4z" },
    editor: { out: "M3 17.25V21h3.75L17.8 9.94l-3.75-3.75zM20.7 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75z", fill: "M3 17.25V21h3.75L17.8 9.94l-3.75-3.75zM20.7 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75z" },
    voices: { out: "M12 14a3 3 0 003-3V5a3 3 0 00-6 0v6a3 3 0 003 3zm5-3a5 5 0 01-10 0H5a7 7 0 006 6.92V21h2v-3.08A7 7 0 0019 11z", fill: "M12 14a3 3 0 003-3V5a3 3 0 00-6 0v6a3 3 0 003 3zm5-3a5 5 0 01-10 0H5a7 7 0 006 6.92V21h2v-3.08A7 7 0 0019 11z" },
    export: { out: "M12 3l7 7h-4v7h-6v-7H5z", fill: "M12 3l7 7h-4v7h-6v-7H5z" },
  };

  const NAV = [
    ["recap", "Recap"], ["editor", "Editor"], ["voices", "Voices"], ["export", "Export"],
  ];

  function navItem(key, label, selected) {
    const g = ICON[key];
    return (
      '<button class="nav-item" data-tab="' + key + '" aria-selected="' + selected + '">' +
        '<span class="pill"></span>' +
        '<svg class="ico-out" viewBox="0 0 24 24" fill="currentColor"><path d="' + g.out + '"/></svg>' +
        '<svg class="ico-fill" viewBox="0 0 24 24" fill="currentColor"><path d="' + g.fill + '"/></svg>' +
        '<span class="lbl">' + label + "</span>" +
      "</button>"
    );
  }

  function injectNavs() {
    document.querySelectorAll("[data-nav]").forEach((nav) => {
      const active = nav.dataset.active || "recap";
      nav.innerHTML = NAV.map(([k, l]) => navItem(k, l, k === active)).join("");
    });
  }

  function injectVoices() {
    const host = document.querySelector("[data-voices]");
    if (!host) return;
    const voices = [
      ["မြန်မာ အမျိုးသမီး ၁", "female", true],
      ["မြန်မာ အမျိုးသမီး ၂", "female", false],
      ["မြန်မာ အမျိုးသား ၁", "male", false],
      ["မြန်မာ အမျိုးသား ၂", "male", false],
      ["မြန်မာ အမျိုးသား ၃", "male", false],
    ];
    host.innerHTML = voices.map(([label, , sel], i) => {
      const bars = Array.from({ length: 20 }, (_, b) =>
        '<span style="animation-delay:' + (b * 0.05).toFixed(2) + 's"></span>'
      ).join("");
      return (
        '<div class="voice-card' + (sel ? " sel" : "") + '">' +
          '<div class="badge"><svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M12 14a3 3 0 003-3V5a3 3 0 00-6 0v6a3 3 0 003 3zm5-3a5 5 0 01-10 0H5a7 7 0 006 6.92V21h2v-3.08A7 7 0 0019 11z"/></svg></div>' +
          '<div class="info"><b class="mm">' + label + '</b><div class="wave">' + bars + "</div></div>" +
          '<button class="playbtn">' + ICON.play + "</button>" +
        "</div>"
      );
    }).join("");
  }

  injectNavs();
  injectVoices();

  /* ---------------------------------------------------- view switching */
  const viewBoard = document.getElementById("view-board");
  const viewProto = document.getElementById("view-proto");
  const tabs = document.querySelectorAll(".view-toggle button");

  function setView(name) {
    const isProto = name === "proto";
    viewBoard.classList.toggle("off", isProto);
    viewProto.classList.toggle("on", isProto);
    tabs.forEach((t) =>
      t.setAttribute("aria-selected", String(t.dataset.view === name))
    );
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
  tabs.forEach((t) =>
    t.addEventListener("click", () => setView(t.dataset.view))
  );

  /* ---------------------------------------------------- phone tab switching
     Every phone in the board shares the same nav markup; clicking a nav
     item swaps the visible screen inside that phone only. */
  document.querySelectorAll(".phone").forEach((phone) => {
    const screens = phone.querySelectorAll("[data-screen]");
    const navItems = phone.querySelectorAll(".nav-item");
    if (!screens.length) return;

    function show(key) {
      screens.forEach((s) => {
        s.style.display = s.dataset.screen === key ? "flex" : "none";
      });
      navItems.forEach((n) =>
        n.setAttribute("aria-selected", String(n.dataset.tab === key))
      );
    }
    navItems.forEach((n) =>
      n.addEventListener("click", () => show(n.dataset.tab))
    );
    const first = phone.querySelector("[data-screen]");
    if (first) show(first.dataset.screen);
  });

  /* ---------------------------------------------------- orb thinking toggle */
  document.querySelectorAll("[data-orb-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const orb = btn.closest(".orb-stage").querySelector(".orb");
      orb.classList.toggle("thinking");
      const on = orb.classList.contains("thinking");
      btn.textContent = on ? "Stop thinking" : "Simulate thinking";
      const cap = btn.closest(".orb-stage").querySelector(".orb-caption .st");
      if (cap) {
        cap.textContent = on
          ? "AssemblyAI · စာသားထုတ်ယူနေသည်…"
          : "3 မိနစ် ရုပ်ရှင် ပြန်လည်ခြုံငုံမှု ဖန်တီးပါ";
      }
    });
  });

  /* ---------------------------------------------------- draggable overlays */
  document.querySelectorAll(".editor-preview").forEach((stage) => {
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
        const startX = e.clientX;
        const startY = e.clientY;
        const baseX = parseFloat(box.dataset.x || "0");
        const baseY = parseFloat(box.dataset.y || "0");

        function move(ev) {
          let nx = baseX + (ev.clientX - startX);
          let ny = baseY + (ev.clientY - startY);
          /* magnetic snap to the 8px safe-area guides */
          const snap = (v, targets, threshold = 8) => {
            for (const t of targets) {
              if (Math.abs(v - t) < threshold) return t;
            }
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
  });

  /* ---------------------------------------------------- voice preview */
  document.querySelectorAll(".voice-card").forEach((card) => {
    const btn = card.querySelector(".playbtn");
    const wave = card.querySelector(".wave");
    if (!btn) return;
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const on = !btn.classList.contains("on");
      btn.classList.toggle("on", on);
      wave && wave.classList.toggle("on", on);
      btn.innerHTML = on ? ICON.pause : ICON.play;
      if (on) {
        setTimeout(() => {
          btn.classList.remove("on");
          wave && wave.classList.remove("on");
          btn.innerHTML = ICON.play;
        }, 3200);
      }
    });
    card.addEventListener("click", () => {
      document.querySelectorAll(".voice-card").forEach((c) => c.classList.remove("sel"));
      card.classList.add("sel");
    });
  });

  /* ---------------------------------------------------- sliders + swatches + segs */
  document.querySelectorAll("[data-live-slider]").forEach((slider) => {
    const out = slider.parentElement.parentElement.querySelector(".val");
    slider.addEventListener("input", () => {
      if (out) out.textContent = slider.value;
      const target = document.querySelector(slider.dataset.liveSlider);
      if (target) target.style.fontSize = slider.value + "px";
    });
  });

  document.querySelectorAll(".swatches").forEach((row) => {
    row.querySelectorAll(".swatch").forEach((sw) => {
      sw.addEventListener("click", () => {
        row.querySelectorAll(".swatch").forEach((s) => s.classList.remove("sel"));
        sw.classList.add("sel");
        const target = document.querySelector(row.dataset.target);
        if (target) target.style.color = sw.dataset.color;
      });
    });
  });

  document.querySelectorAll(".seg").forEach((seg) => {
    seg.querySelectorAll("button").forEach((b) => {
      b.addEventListener("click", () => {
        seg.querySelectorAll("button").forEach((x) =>
          x.setAttribute("aria-selected", "false")
        );
        b.setAttribute("aria-selected", "true");
      });
    });
  });

  document.querySelectorAll(".fontrow").forEach((row) => {
    row.querySelectorAll(".fontbtn").forEach((b) => {
      b.addEventListener("click", () => {
        row.querySelectorAll(".fontbtn").forEach((x) => x.classList.remove("sel"));
        b.classList.add("sel");
        const target = document.querySelector(row.dataset.target);
        if (target) target.style.fontFamily = b.dataset.font;
      });
    });
  });

  /* ---------------------------------------------------- export bloom */
  document.querySelectorAll(".export-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const bloom = btn.querySelector(".bloom");
      if (!bloom) return;
      bloom.classList.remove("go");
      void bloom.offsetWidth; /* restart the animation */
      bloom.classList.add("go");
      const ring = document.querySelector(".ring .pct");
      if (ring) {
        let p = 0;
        const id = setInterval(() => {
          p = Math.min(100, p + 7);
          ring.textContent = p + "%";
          if (p >= 100) {
            clearInterval(id);
            ring.textContent = "✓";
          }
        }, 90);
      }
    });
  });

  /* ---------------------------------------------------- skeleton → content */
  document.querySelectorAll("[data-skeleton]").forEach((host) => {
    const lines = host.querySelectorAll(".skel");
    lines.forEach((l, i) => {
      setTimeout(() => {
        l.classList.add("line-in");
        l.style.background = "none";
        l.style.height = "auto";
        l.innerHTML = l.dataset.text || "";
      }, 900 + i * 60);
    });
  });

  /* ---------------------------------------------------- dialog buttons */
  document.querySelectorAll("[data-close-dialog]").forEach((b) => {
    b.addEventListener("click", () => {
      const scrim = b.closest(".scrim");
      if (scrim) scrim.style.display = "none";
    });
  });

})();
