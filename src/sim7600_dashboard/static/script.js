// SIM7600 Dashboard JavaScript

let contacts = [];

// Update status on page load
document.addEventListener("DOMContentLoaded", function () {
  updateStatus();
  loadMessages();
  loadContacts();

  // Auto-refresh messages every 5 seconds
  setInterval(loadMessages, 5000);

  // Auto-update status every 3 seconds
  setInterval(updateStatus, 3000);

  // Character counter
  const messageInput = document.getElementById("message");
  const charCount = document.getElementById("charCount");

  messageInput.addEventListener("input", function () {
    charCount.textContent = this.value.length;

    // Check for non-ASCII characters
    checkSpecialCharacters(this.value);
  });

  // Form submission
  document.getElementById("sendForm").addEventListener("submit", sendSMS);

  // Phone autocomplete
  setupAutocomplete();
});

// Update connection status
async function updateStatus() {
  try {
    const response = await fetch("/api/status");
    const data = await response.json();

    const statusEl = document.getElementById("status");
    const portEl = document.getElementById("port");
    const countEl = document.getElementById("message-count");

    if (data.connected) {
      statusEl.className = "status connected";
      statusEl.textContent = "● Connected";
      portEl.textContent = `Port: ${data.port}`;
    } else {
      statusEl.className = "status disconnected";
      statusEl.textContent = "● Disconnected";
      portEl.textContent = "No modem detected";
    }

    countEl.textContent = `${data.message_count} messages`;
  } catch (error) {
    console.error("Error updating status:", error);
  }
}

// Load messages
async function loadMessages() {
  try {
    const response = await fetch("/api/messages");
    const data = await response.json();

    const messagesList = document.getElementById("messagesList");

    if (data.messages.length === 0) {
      messagesList.innerHTML = '<div class="no-messages">No messages yet</div>';
      return;
    }

    messagesList.innerHTML = data.messages
      .map((msg) => {
        const isSent = msg.direction === "sent";
        const contact = isSent ? msg.recipient : msg.sender;
        const time = isSent
          ? new Date(msg.timestamp).toLocaleString()
          : formatTimestamp(msg.timestamp);
        const directionIcon = isSent ? "📤" : "📥";
        const itemClass = isSent ? "message-item sent" : "message-item";

        return `
            <div class="${itemClass}">
                <div class="message-header">
                    <span class="message-sender">${directionIcon} ${
          isSent ? "To: " : ""
        }${escapeHtml(contact)}</span>
                    <span class="message-time">${time}</span>
                </div>
                <div class="message-text">${escapeHtml(msg.text)}</div>
            </div>
        `;
      })
      .join("");
  } catch (error) {
    console.error("Error loading messages:", error);
  }
}

// Refresh messages (called by button)
function refreshMessages() {
  loadMessages();
  showStatus("Messages refreshed", "success");
}

// Send SMS
async function sendSMS(e) {
  e.preventDefault();

  const phone = document.getElementById("phone").value.trim();
  const message = document.getElementById("message").value.trim();

  if (!phone || !message) {
    showStatus("Please fill in all fields", "error");
    return;
  }

  const sendBtn = e.target.querySelector('button[type="submit"]');
  sendBtn.disabled = true;
  sendBtn.textContent = "Sending...";

  try {
    const response = await fetch("/api/send", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ phone, message }),
    });

    const data = await response.json();

    if (data.success) {
      showStatus("✅ SMS sent successfully!", "success");
      clearForm();

      if (!data.ascii_only && data.preview) {
        showStatus(
          `SMS sent. Special characters were converted. Sent as: "${data.preview}"`,
          "success"
        );
      }
    } else {
      showStatus(`❌ Error: ${data.error}`, "error");
    }
  } catch (error) {
    showStatus(`❌ Error: ${error.message}`, "error");
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = "Send SMS";
  }
}

// Check for special characters
function checkSpecialCharacters(message) {
  const warningDiv = document.getElementById("warning");
  const previewDiv = document.getElementById("preview");

  // Try to encode as ASCII
  let hasSpecialChars = false;
  for (let char of message) {
    if (char.charCodeAt(0) > 127) {
      hasSpecialChars = true;
      break;
    }
  }

  if (hasSpecialChars) {
    // Show warning
    const preview = message
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^\x00-\x7F]/g, "?");
    warningDiv.style.display = "block";
    previewDiv.innerHTML = `Message will be sent as: <strong>"${escapeHtml(
      preview
    )}"</strong>`;
  } else {
    warningDiv.style.display = "none";
  }
}

// Show status message
function showStatus(message, type) {
  const statusDiv = document.getElementById("sendStatus");
  statusDiv.textContent = message;
  statusDiv.className = `status-message ${type}`;

  // Hide after 5 seconds
  setTimeout(() => {
    statusDiv.style.display = "none";
  }, 5000);
}

// Clear form
function clearForm() {
  document.getElementById("phone").value = "";
  document.getElementById("message").value = "";
  document.getElementById("charCount").textContent = "0";
  document.getElementById("warning").style.display = "none";
}

// Format timestamp
function formatTimestamp(timestamp) {
  // Format: 25/10/18,20:08:02+08
  try {
    const parts = timestamp.split(",");
    if (parts.length === 2) {
      const dateParts = parts[0].split("/");
      const timePart = parts[1].substring(0, 8);
      return `${dateParts[0]}/${dateParts[1]} ${timePart}`;
    }
  } catch (e) {
    // Fallback
  }
  return timestamp;
}

// Escape HTML
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Load contacts for autocomplete
async function loadContacts() {
  try {
    const response = await fetch("/api/contacts");
    const data = await response.json();
    contacts = data.contacts;
  } catch (error) {
    console.error("Error loading contacts:", error);
  }
}

// Setup phone number autocomplete
function setupAutocomplete() {
  const phoneInput = document.getElementById("phone");
  const suggestionsDiv = document.getElementById("suggestions");

  phoneInput.addEventListener("input", function () {
    const value = this.value.toLowerCase();
    suggestionsDiv.innerHTML = "";

    if (value.length === 0) {
      suggestionsDiv.style.display = "none";
      return;
    }

    const matches = contacts.filter((contact) =>
      contact.toLowerCase().includes(value)
    );

    if (matches.length > 0) {
      suggestionsDiv.style.display = "block";
      matches.slice(0, 5).forEach((contact) => {
        const div = document.createElement("div");
        div.className = "suggestion-item";
        div.textContent = contact;
        div.addEventListener("click", function () {
          phoneInput.value = contact;
          suggestionsDiv.style.display = "none";
        });
        suggestionsDiv.appendChild(div);
      });
    } else {
      suggestionsDiv.style.display = "none";
    }
  });

  // Hide suggestions when clicking outside
  document.addEventListener("click", function (e) {
    if (e.target !== phoneInput) {
      suggestionsDiv.style.display = "none";
    }
  });

  // Handle keyboard navigation
  phoneInput.addEventListener("keydown", function (e) {
    const items = suggestionsDiv.querySelectorAll(".suggestion-item");
    if (items.length === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      items[0].focus();
    }
  });
}
