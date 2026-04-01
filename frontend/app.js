const API_BASE = "https://w4o4c1pz78.execute-api.us-east-2.amazonaws.com/prod";

/* ── SUBMIT ── */
document.getElementById("submitForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = document.getElementById("submitBtn");
  const err = document.getElementById("submitErr");

  btn.disabled = true;
  btn.innerHTML = "<span>Submitting…</span>";
  err.classList.remove("show");

  const data = {
    name:        document.getElementById("name").value,
    email:       document.getElementById("email").value,
    location:    document.getElementById("location").value,
    description: document.getElementById("description").value,
  };

  try {
    const res = await fetch(`${API_BASE}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error();
    const result = await res.json();

    // Handles any key the API might return: requestId, request_id, id, etc.
    const id = result.requestId || result.request_id || result.id || Object.values(result)[0] || "—";

    document.getElementById("submitForm").style.display = "none";
    document.getElementById("successBox").classList.add("show");
    document.getElementById("genId").textContent = id;
  } catch {
    err.classList.add("show");
    btn.disabled = false;
    btn.innerHTML = "<span>Submit Request</span><span>→</span>";
  }
});

/* ── TRACK ── */
async function trackRequest() {
  const id    = document.getElementById("requestId").value.trim();
  const err   = document.getElementById("trackErr");
  const btn   = document.getElementById("trackBtn");
  const empty = document.getElementById("emptyState");
  const inner = document.getElementById("resultInner");

  err.classList.remove("show");
  inner.classList.remove("show");
  if (!id) return;

  btn.disabled = true;
  btn.textContent = "Checking…";

  try {
    const res  = await fetch(`${API_BASE}/track?id=${encodeURIComponent(id)}`);
    const data = await res.json();
    if (data.error || data.message) throw new Error();

    document.getElementById("dispId").textContent    = data.request_id || data.requestId || id;
    document.getElementById("dispName").textContent  = data.name        || "—";
    document.getElementById("dispEmail").textContent = data.email       || "—";
    document.getElementById("dispLoc").textContent   = data.location    || "—";
    document.getElementById("dispDesc").textContent  = data.description || "—";

    const status = (data.status || "pending").toLowerCase();
    const chip   = document.getElementById("dispChip");
    if (status.includes("progress")) {
      chip.textContent = "In Progress"; chip.className = "chip chip-progress";
    } else if (status.includes("complet") || status.includes("resolv") || status.includes("done")) {
      chip.textContent = "Resolved";    chip.className = "chip chip-done";
    } else {
      chip.textContent = "Pending";     chip.className = "chip chip-pending";
    }

    // progress indicator
    const dots  = ["pd1","pd2","pd3"].map(i => document.getElementById(i));
    const lines = ["pl1","pl2"].map(i => document.getElementById(i));
    const steps = ["ps1","ps2","ps3"].map(i => document.getElementById(i));
    dots.forEach(d  => d.classList.remove("done","active"));
    lines.forEach(l => l.classList.remove("done"));
    steps.forEach(s => s.classList.remove("done","active"));

    if (status.includes("progress")) {
      steps[0].classList.add("done");   dots[0].classList.add("done");  lines[0].classList.add("done");
      steps[1].classList.add("active"); dots[1].classList.add("active");
    } else if (status.includes("complet") || status.includes("resolv") || status.includes("done")) {
      steps.forEach((s,i) => { s.classList.add("done"); dots[i].classList.add("done"); });
      lines.forEach(l => l.classList.add("done"));
    } else {
      steps[0].classList.add("active"); dots[0].classList.add("active");
    }

    if (empty) empty.style.display = "none";
    inner.classList.add("show");
  } catch {
    err.classList.add("show");
  } finally {
    btn.disabled = false;
    btn.textContent = "Check Status";
  }
}
