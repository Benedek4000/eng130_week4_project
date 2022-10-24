// Create function to validate a login form

function validateLoginForm() {
    // Get the email and password from the form
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Check if the email and password are empty

    if (email == "" || password == "") {
        alert("Please enter your email and password");
        return false;
    }
    // Check if the email is valid

    if (!validateEmail(email)) {
        alert("Please enter a valid email");
        return false;
    }

}

function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}