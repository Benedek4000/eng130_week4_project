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

function validateSignUpForm() {
    // Get the email and password from the form
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var comPassword = document.getElementById("confirmPassword").value;

    // Check if all feilds are empty

    if (firstName == "" || lastName == "" || email == "" || password == "" || comPassword == "") {
        // Return Error Message if email and password is empty
        alert("Please enter all fields");
        return false;
    }
    if (validatePassword() == True && validateEmail() == True) {
        
    }

}

// Create fuction that vaildates the sign up form and then sends the data to the backend in a JSON format
// Get form data from the form
// Use a event listener to listen for the submit event
// Disable the default action of the submit event
// Use fetch to post the data to the backend

function newSignUpForm(){
    const signUpForm = document.getElementById("signUpForm");
    signUpForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(signUpForm);
        const data = Object.fromEntries(formData);
        const jsonData = JSON.stringify(data);
        console.log(jsonData);
    
    })
}




function validatePassword() {
    var pass = document.getElementById("password");
    var comPass = document.getElementById("confirmPassword");
    if (pass.value != comPass.value) {
        alert("Passwords do not match");
        return false;
    }
    if (pass.value.length < 8) {
        alert("Password must be at least 8 characters");
        return false;
    }
    if (pass.value.search(/[a-z]/i) < 0) {
        alert("Password must contain at least one letter");
        return false;
    }
    if (pass.value.search(/[0-9]/) < 0) {
        alert("Password must contain at least one digit");
        return false;
    }
    if (pass.value.search(/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/) < 0) {
        alert("Password must contain at least one special character");
        return false;
    }
    else {
        return true;
    }
}

function validateEmail() {
    var email = document.getElementById("email");
    if (email.value.search(/@/) < 0) {
        alert("Email must contain @");
        return false;
    }
    if (email.value.search(/.com/) < 0) {
        alert("Email must contain .com");
        return false;
    }
    else{
        return true;
    }
}


function showPassword() {
    var pass = document.getElementById("password");
    var comPass = document.getElementById("confirmPassword");
    var eye = document.getElementById("eye-icon");
    if (pass.type === "password") {
        pass.type = "text";
        comPass.type = "text";
        eye.className = "fa-sharp fa-solid fa-eye-slash";
    } else {
        pass.type = "password";
        comPass.type = "password";
        eye.className = "fa-sharp fa-solid fa-eye";
    }
  }