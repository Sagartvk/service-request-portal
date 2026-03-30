const API_BASE = "https://w4o4c1pz78.execute-api.us-east-2.amazonaws.com/prod";

/* SUBMIT */
async function submitRequest() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const location = document.getElementById("location").value;
  const description = document.getElementById("description").value;

  const messageDiv = document.getElementById("message");

  try {
    const response = await fetch(`${API_BASE}/submit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name, email, location, description })
    });

    const data = await response.json();

    messageDiv.innerHTML = `
      <div class="message success">
        ✅ Submitted! <br>ID: ${data.request_id}
      </div>
    `;
  } catch (err) {
    messageDiv.innerHTML = `
      <div class="message error">
        ❌ Submission failed
      </div>
    `;
  }
}

/* TRACK */
async function trackRequest() {
  const id = document.getElementById("requestId").value;
  const resultDiv = document.getElementById("result");

  try {
    const response = await fetch(`${API_BASE}/track?id=${id}`);
    const data = await response.json();

    if (data.error || data.message) {
      resultDiv.innerHTML = `
        <div class="message error">
          ❌ ${data.error || data.message}
        </div>
      `;
      return;
    }

    resultDiv.innerHTML = `
      <div class="card">
        <p><strong>ID:</strong> ${data.request_id}</p>
        <p><strong>Name:</strong> ${data.name}</p>
        <p><strong>Location:</strong> ${data.location}</p>
        <p><strong>Description:</strong> ${data.description}</p>
        <p><strong>Status:</strong> ${data.status}</p>
      </div>
    `;
  } catch (error) {
    resultDiv.innerHTML = `
      <div class="message error">
        ❌ Error fetching request
      </div>
    `;
  }
}
