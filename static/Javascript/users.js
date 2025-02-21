function openModal(username, email, role) {
    // Set the values of the form inputs
    document.getElementById('user').value = username;  
    document.getElementById('username').value = username;  
    document.getElementById('email').value = email; 
    document.getElementById('role').value = role;  

    document.getElementById('editModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

async function updateUser(event) {
    event.preventDefault(); 

    const user = document.getElementById('user').value;
    const role = document.getElementById('role').value;

    try {
        const response = await fetch('/update_user', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user, role }),
        });

        const data = await response.json(); 
        const messageDiv = document.getElementById('message');
        
        if (response.ok) {
            messageDiv.textContent = data.detail;  
            messageDiv.className = 'message success'; 
            messageDiv.style.display = 'block';  
            closeModal();
            location.reload();  // Refresh page after update
        } else {
            messageDiv.textContent = "Error updating user: " + data.detail; 
            messageDiv.className = 'message error';  
            messageDiv.style.display = 'block';  
        }
    } catch (error) {
        console.error("Error:", error);
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = "An error occurred while updating the user.";  
        messageDiv.className = 'message error';  
        messageDiv.style.display = 'block';  
    }
}


function logout(event) {
    event.preventDefault();  
    // localStorage.removeItem("access_token");

    fetch("/logout", {
        method: "POST", 
        credentials: "same-origin",  
        headers: {
            "Content-Type": "application/json"  
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/login";
        } else {
            throw new Error("Logout failed");
        }
    })
    .catch(error => {
        console.error("Logout error:", error);
    });
}
