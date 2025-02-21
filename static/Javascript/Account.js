function logout(event) {
    event.preventDefault();  
  
    
    // document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC";

  
   
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
  
  