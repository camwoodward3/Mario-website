const tabLogin = document.getElementById("tab-login");
const tabSignup = document.getElementById("tab-signup");
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");
const statusMsg = document.getElementById("auth-status");

// Check if user is already logged in; if so, skip to index.html
async function checkCurrentSession() {
  try {
    const res = await fetch("/api/me");
    if (!res.ok) {
      return;
    }
    const data = await res.json();
    if (data.loggedIn) {
      window.location.href = "sort.html";
    }
  } catch (err) {
    console.error("Session check failed:", err);
  }
}
checkCurrentSession();

// Tab switching
tabLogin.addEventListener("click", () => {
  tabLogin.classList.add("active");
  tabSignup.classList.remove("active");
  loginForm.classList.remove("hidden");
  signupForm.classList.add("hidden");
  statusMsg.textContent = "";
});

tabSignup.addEventListener("click", () => {
  tabSignup.classList.add("active");
  tabLogin.classList.remove("active");
  signupForm.classList.remove("hidden");
  loginForm.classList.add("hidden");
  statusMsg.textContent = "";
});

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("login-username").value.trim();
  const password = document.getElementById("login-password").value;

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();

    if (!res.ok) {
      statusMsg.className = "status-msg error";
      statusMsg.textContent = data.error || "Login failed.";
      return;
    }

    // Redirect to the main catalog page
    window.location.href = "index.html";
  } catch(err) {
    statusMsg.className = "status-msg error";
    statusMsg.textContent = "Unable to connect to the server.";
  }
});

// Submit Sign Up
signupForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("signup-username").value.trim();
  const password = document.getElementById("signup-password").value;

  try {
    const res = await fetch("/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();

    if (!res.ok) {
      statusMsg.className = "status-msg error";
      statusMsg.textContent = data.error || "Sign up failed.";
      return;
    }

    // Log the user in right after sign up
    const loginRes = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (loginRes.ok) {
      window.location.href = "index.html";
    } else {
      statusMsg.className = "status-msg success";
      statusMsg.textContent = "Account created! Please switch to log in.";
    }
  } catch (err) {
    statusMsg.className = "status-msg error";
    statusMsg.textContent = "Unable to connect to the server.";
  }
});