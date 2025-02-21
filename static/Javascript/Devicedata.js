document.addEventListener("DOMContentLoaded", function () {
    function getAuthHeaders() {
        // const token = localStorage.getItem("access_token");
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }

    function displayError(message) {
        const errorMessageElement = document.getElementById("error_message");
        errorMessageElement.textContent = message;
    }

    
    async function fetchFilteredDeviceData(deviceId) {
        const apiUrl = "/devicedata-fetch";  

        try {
            const headers = getAuthHeaders();
            if (!headers) return;
    
            const response = await fetch(apiUrl, {
                method: "POST",  
                headers: headers,
                body: JSON.stringify({ Device_ID: deviceId })
            });

            if (!response.ok) {
                const errorMessage = await response.text();
                displayError(`Error fetching filtered device data: ${response.status} - ${errorMessage}`);
                return;
            }

            const data = await response.json();
            console.log("Filtered Data Response:", data);
    
            if (data.device_data && Array.isArray(data.device_data)) {
                if (data.device_data.length === 0) {
                    
                    displayError("No data found for the selected Device ID.");
                } else {
                    displayError("");  
                    populateTable(data.device_data);
                }
            } else {
                displayError("Unexpected response format.");
            }
        } catch (error) {
            console.error("Error:", error);
            displayError(`An error occurred while fetching filtered device data: ${error.message}`);
        }
    }

    
    function populateTable(data) {
        const tableBody = document.querySelector("#device-data-table tbody");
        tableBody.innerHTML = "";

        data.forEach(device => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${device.Device_Id || "N/A"}</td>
                <td>${device.Battery_Level || "N/A"}</td>
                <td>${device.First_Sensor_temperature || "N/A"}</td>
                <td>${device.Route_From || "N/A"}</td>
                <td>${device.Route_To || "N/A"}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    
    const submitButton = document.getElementById("submit");
    if (submitButton) {
        submitButton.addEventListener("click", function () {
            const deviceId = document.getElementById("device_id").value.trim();
            if (!deviceId) {
                displayError("Please select a Device ID.");
                return;
            }
            fetchFilteredDeviceData(deviceId);
        });
    } else {
        console.error("Submit button not found.");
    }

    
    const refreshButton = document.getElementById("refresh");
    if (refreshButton) {
        refreshButton.addEventListener("click", function () {
            window.location.reload();  
        });
    } else {
        console.error("Refresh button not found.");
    }
});


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
        Error("Error logging out. Please try again.");
    });
}
