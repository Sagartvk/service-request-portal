const SUBMIT_API = "https://w4o4c1pz78.execute-api.us-east-2.amazonaws.com/prod/submit";
const TRACK_API = "https://w4o4c1pz78.execute-api.us-east-2.amazonaws.com/prod/track";

const form = document.getElementById("form");
const msg = document.getElementById("msg");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            location: document.getElementById("location").value,
            description: document.getElementById("desc").value
        };

        const res = await fetch(SUBMIT_API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        const parsed = typeof result.body === "string" ? JSON.parse(result.body) : result;

        msg.innerText = "ID: " + parsed.request_id;
        form.reset();
    });
}

async function track() {
    const trackInput = document.getElementById("id");
    const resultBox = document.getElementById("result");

    const res = await fetch(`${TRACK_API}?id=${trackInput.value}`);
    const result = await res.json();
    const parsed = typeof result.body === "string" ? JSON.parse(result.body) : result;

    resultBox.innerText = JSON.stringify(parsed, null, 2);
}
