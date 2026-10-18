const marioList = document.getElementById("mario-list");
let mario = [];

const menuToggle = document.getElementById("menu-toggle");
const navContainer = document.getElementById("nav-container");

if (menuToggle && navContainer) {
  menuToggle.addEventListener("click", () => {
    navContainer.classList.toggle("open");
  });
}

function countAppearances(character) {
  let count = 0;
  const categories = [
    "consoles", "handheld", "hybrid", "arcade", "computer", "mobile", "games", "toys", "figurines"
  ];

  categories.forEach(cat => {
    if (character[cat]) {
      Object.values(character[cat]).forEach(arr => {
        if (Array.isArray(arr)) count += arr.length;
      });
    }
  });
  return count;
}

function getPlatforms(character) {
  const platforms = new Set();
  const categories = [
    "consoles", "handheld", "hybrid", "arcade", "computer", "mobile"
  ];

  categories.forEach(cat => {
    if (character[cat]) {
      Object.keys(character[cat]).forEach(system => platforms.add(system));
    }
  });

  return Array.from(platforms);
}

async function init() {
  try {
    const files = [
      "mario/characters2.json",
      "mario/enemies2.json"
    ];

    const dataArrays = await Promise.all(files.map(url => fetch(url).then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status} on ${url}`);
      return res.json();
    }))
    );

    mario = dataArrays.flatMap(data => Object.entries(data).map(([id, item]) => ({ id, ...item,
      total: countAppearances(item),
      platformList: getPlatforms(item)
    }))
  );

  populateDropdowns();
  render(mario);
  setupEventListeners();
  } catch (err) {
    console.error("Failed to load character data:", err);
  }
}

function render(data) {
  if (!marioList) return;
  marioList.innerHTML = data.map(item => {
    return `
    <div class="character">
    <button data-id="${item.id}">${item.name || item.id}</button>
    </div>
    `;
  }).join("");
}

function populateDropdowns() {
  const allPlatforms = mario.flatMap(m => m.platformList);
  fillSelect("#console", allPlatforms);

  const totalSelect = document.querySelector("#total");
  if (totalSelect) {
    totalSelect.innerHTML = `
      <option value="all"></option>
      <option value="1">1(Rare)</option>
      <option value="2-10">2 - 10</option>
      <option value="11-50">11 - 50</option>
      <option value="50+">50+</option>
    `;
  }

}

function fillSelect(selector, values) {
  const select = document.querySelector(selector);
  if (!select) return;

  select.innerHTML = `<option value="all">All Consoles</option>`;

  [...new Set(values.filter(Boolean))].sort().forEach(val => {
    select.innerHTML += `<option value="${val}">${val}</option>`;
  });
}

function setupEventListeners() {
  document.querySelectorAll("select").forEach(select => {
    select.addEventListener("change", applyFiltersAndSort);
  });
}
function applyFiltersAndSort() {
      const totalSelect = document.querySelector("#total")?.value || "all";
      const consoleSelect = document.querySelector("#console")?.value || "all";
      const sortSelect = document.querySelector("#sort-order")?.value || "none";
  
      let result = mario.filter(m => {
        const consoleMatch =
          consoleSelect === "all" || m.platformList.includes(consoleSelect);
 
         let totalMatch = true;
         if (totalSelect === "1") totalMatch = m.total === 1;
         else if (totalSelect === "2-10") totalMatch = m.total >= 2 && m.total <= 10;
         else if (totalSelect === "11-50") totalMatch = m.total >= 11 && m.total <= 50;
         else if (totalSelect === "50+") totalMatch = m.total > 50;
   
         return totalMatch && consoleMatch;
      });
      
      if (sortSelect === "asc") {
        // Least to most appearances
        result.sort((a, b) => a.total - b.total);
      } else if (sortSelect === "desc") {
        // Most to least appearances
        result.sort((a, b) => b.total - a.total);
      }
      render(result);
  }

// Sign up
async function handleSignup(username, password) {
  const res = await fetch('/api/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return res.json();
}

// Log in
async function handleLogin(username, password) {
  const res = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return res.json();
}

// Log out 
async function handleLogout() {
  const res = await fetch('/api/logout', { method: 'POST' });
  return res.json();
}

async function guardPage() {
  try {
    const res = await fetch("/api/me");

    if (!res.ok) {
      window.location.href = "login.html";
      return;
    }
    
    const data = await res.json();

    if (!data.loggedIn) {
      // Not logged in -> kick them out to login.html
      window.location.href = "login.html";
      return;
    }

    // If authenticated, display user and initialize the Mario app
    const greeting = document.getElementById("user-greeting");
    if (greeting) greeting.textContent = `Logged in as ${data.username}`;
    
    init(); // Run your character loading logic
  } catch (err) {
    window.location.href = "login.html";
  }
}

const logoutBtn = document.getElementById("logout-btn");

if (!logoutBtn) {
  console.error("Logout button was NOT found in the DOM!");
} else {
  console.log("Logout button was successfully found.");
  
  logoutBtn.addEventListener("click", async () => {
    console.log("Logout button was clicked!");
    
    try {
      const res = await fetch("/api/logout", { method: "POST" });
      console.log("Server responded with status:", res.status);

      if (res.ok) {
        window.location.href = "login.html";
      } else {
        console.error("Logout failed on server:", await res.text());
      }
    } catch (err) {
      console.error("Network error during logout:", err);
    }
  });
}


guardPage();

