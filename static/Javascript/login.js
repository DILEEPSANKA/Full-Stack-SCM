let captchaCode = "";


function generateCaptcha() {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let code = "";
  for (let i = 0; i < 6; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  captchaCode = code;
  document.getElementById("captchaPreview").textContent = captchaCode; 
}


window.addEventListener('load', () => {
  generateCaptcha(); 
});

document.getElementById("login-form").addEventListener("submit", async function (event) {
  event.preventDefault(); 

  
  const captchaInput = document.getElementById("captcha").value;

  
  if (captchaInput !== captchaCode) {
    const captchaErrorElement = document.getElementById("captchaError");
    captchaErrorElement.style.display = "block";

    return;
  }


  const form = document.getElementById("login-form");
  const formData = new FormData(form);

  try {
    const response = await fetch("/login", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      
      const token = data.access_token;
      localStorage.setItem("access_token", token);
      window.location.href = "/dashboard";
    } else {
      const errorData = await response.json();
      displayError(errorData.detail || "Invalid username or password.");
    }
  } catch (error) {
    displayError("An error occurred during the login process. Please try again.");
    console.error("Login error:", error);
  }
});

function displayError(message) {
  const errorMessage = document.createElement("div");
  errorMessage.classList.add("form-alert", "alert-error");
  errorMessage.textContent = message;
  const form = document.getElementById("login-form");
  form.insertBefore(errorMessage, form.firstChild); 
  
  setTimeout(() => {
    errorMessage.style.display = "none";
  }, 5000);
}
