const formSignUp = document.getElementById('signUpForm');

if (formSignUp) {
	formSignUp.addEventListener('submit', (e) => {
		e.preventDefault();

		// Get form data from the form
		var firstName = document.getElementById('firstName').value;
		var lastName = document.getElementById('lastName').value;
		var email = document.getElementById('email').value;
		var password = document.getElementById('password').value;
		var comPassword = document.getElementById('confirmPassword').value;
		//stringify the data

		const data = JSON.stringify({
			firstName,
			lastName,
			email,
			password,
			comPassword,
		});

		console.log(data);

		// Send the data to the server
		// fetch('/api/signup', {
		// 	method: 'POST',
		// 	headers: {
		// 		'Content-Type': 'application/json',
		// 	},
		// 	body: data,
		// });
	});
} else {
	console.log('The Form is not found');
}

function validateLoginForm() {
	// Get the email and password from the form
	var email = document.getElementById('email').value;
	var password = document.getElementById('password').value;

	// Check if email and password is empty
	if (email == '' || password == '') {
		// Return Error Message if email and password is empty
		alert('Please enter your email and password');
		return false;
	}
}


function validateSignUpForm() {
	// Get the email and password from the form
	var firstName = document.getElementById('firstName').value;
	var lastName = document.getElementById('lastName').value;
	var email = document.getElementById('email').value;
	var password = document.getElementById('password').value;
	var comPassword = document.getElementById('confirmPassword').value;

	// Check if all feilds are empty

	if (firstName == '' || lastName == '' || email == '' || password == '' || comPassword == '') {
		// Return Error Message if email and password is empty
		alert('Please enter all fields');
		return false;
	}
	validatePassword();
	validateEmail();
}

function validatePassword() {
	var pass = document.getElementById('password');
	var comPass = document.getElementById('confirmPassword');
	if (pass.value != comPass.value) {
		alert('Passwords do not match');
		return false;
	}
	if (pass.value.length < 8) {
		alert('Password must be at least 8 characters');
		return false;
	}
	if (pass.value.search(/[a-z]/i) < 0) {
		alert('Password must contain at least one letter');
		return false;
	}
	if (pass.value.search(/[0-9]/) < 0) {
		alert('Password must contain at least one digit');
		return false;
	}
	if (pass.value.search(/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/) < 0) {
		alert('Password must contain at least one special character');
		return false;
	} else {
		return true;
	}
}

function validateEmail() {
	var email = document.getElementById('email');
	if (email.value.search(/@/) < 0) {
		alert('Email must contain @');
		return false;
	}
	if (email.value.search(/.com/) < 0) {
		alert('Email must contain .com');
		return false;
	} else {
		return true;
	}
}

function showPassword() {
	var pass = document.getElementById('password');
	var comPass = document.getElementById('confirmPassword');
	var eye = document.getElementById('eye-icon');
	if (pass.type === 'password') {
		pass.type = 'text';
		comPass.type = 'text';
		eye.className = 'fa-sharp fa-solid fa-eye-slash';
	} else {
		pass.type = 'password';
		comPass.type = 'password';
		eye.className = 'fa-sharp fa-solid fa-eye';
	}
}
