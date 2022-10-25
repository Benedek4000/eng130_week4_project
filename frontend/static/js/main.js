// Create function to validate a login form, for email and password
// Check if email and password is empty
// Check if the email and password are valid
// Return Error Message if email and password is empty
// Return Error Message if email and password is invalid


function validateLoginForm() {
    // Get the email and password from the form
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Check if email and password is empty
    if (email == "" || password == "") {
        // Return Error Message if email and password is empty
        alert("Please enter your email and password");
        return false;
    }

    
}

   
