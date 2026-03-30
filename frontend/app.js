const API_BASE = "https://w4o4c1pz78.execute-api.us-east-2.amazonaws.com/prod";

/* ── SUBMIT ─────────────────────────────────────────────── */
document.getElementById("submitForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const btn = e.target.querySelector("button[type=submit]");
    btn.textContent = "Submitting";
    btn.disabled = true;

    const errorEl = document.getElementById("submitError");
    errorEl.classList.remove("visible");

    const data = {
        name:        document.getElementById("name").value,
        email:       document.getElementById("email").value,
        location:    document.getElementById("location").value,
        description: document.getElementById("description").value
    };

    try {
        const res    = await fetch(`${API_BASE}/submit`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify(data)
        });

        if (!res.ok) throw new Error("API error");

        const result = await res.json();

        document.getElementById("submitForm").style.display         = "none";
        document.querySelector(".card-header").style.display        = "none";
        document.getElementById("successMessage").classList.add("visible");
        document.getElementById("generatedId").innerText            = result.request_id;

    } catch {
        errorEl.classList.add("visible");
        btn.textContent = "Submit Request";
        btn.disabled    = false;
    }
});


/* ── TRACK ──────────────────────────────────────────────── */
async function trackRequest() {
    const id      = document.getElementById("requestId").value.trim();
    const errorEl = document.getElementById("trackError");
    const cardEl  = document.getElementById("statusCard");

    errorEl.classList.remove("visible");
    cardEl.classList.remove("visible");

    if (!id) return;

    const btn = document.querySelector(".btn-primary");
    btn.textContent = "Tracking";
    btn.disabled    = true;

    try {
        const res  = await fetch(`${API_BASE}/track?id=${encodeURIComponent(id)}`);
        const data = await res.json();

        if (data.error || data.message) throw new Error("Not found");

        document.getElementById("displayId").textContent          = data.request_id;
        document.getElementById("displayName").textContent        = data.name        || "—";
        document.getElementById("displayEmail").textContent       = data.email       || "—";
        document.getElementById("displayLocation").textContent    = data.location    || "—";
        document.getElementById("displayDescription").textContent = data.description || "—";

        const badge   = document.getElementById("statusBadge");
        const status  = (data.status || "pending").toLowerCase();
        badge.textContent = data.status || "Pending";
        badge.className   = "status-badge " + (
            status.includes("progress") ? "status-progress" :
            status.includes("complet")  ? "status-completed" :
            "status-pending"
        );

        cardEl.classList.add("visible");

    } catch {
        errorEl.classList.add("visible");
    } finally {
        btn.textContent = "Track Status";
        btn.disabled    = false;
    }
}
