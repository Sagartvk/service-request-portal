const API_BASE = "https://w4o4c1pz78.execute-api.us-east-2.amazonaws.com/prod";

/* SUBMIT */
document.getElementById("submitForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    location: document.getElementById("location").value,
    description: document.getElementById("description").value
  };

  const res = await fetch(`${API_BASE}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();

  document.getElementById("submitForm").style.display = "none";
  document.getElementById("successMessage").classList.add("visible");
  document.getElementById("generatedId").innerText = result.request_id;
});


/* TRACK */
async function trackRequest() {
  const id = document.getElementById("requestId").value;

  const res = await fetch(`${API_BASE}/track?id=${id}`);
  const data = await res.json();

  const resultDiv = document.getElementById("result");

  if (data.error || data.message) {
    resultDiv.innerHTML = `<p style="color:red;">Error loading request</p>`;
    return;
  }

  resultDiv.innerHTML = `
    <div class="status-card visible">
      <div class="status-header">
        <span>${data.request_id}</span>
        <span>${data.status}</span>
      </div>
      <p><b>Name:</b> ${data.name}</p>
      <p><b>Email:</b> ${data.email}</p>
      <p><b>Location:</b> ${data.location}</p>
      <p><b>Description:</b> ${data.description}</p>
    </div>
  `;
}
