// script.js

const email = document.getElementById("email");
const password = document.getElementById("password");
const message = document.getElementById("message");

// Email/password login
function login() {
  firebase.auth().signInWithEmailAndPassword(email.value, password.value)
    .then((userCredential) => {
      alert("Successfully logged in!");
      message.innerText = "Login successful!";
    })
    .catch((error) => {
      message.innerText = error.message;
    });
}

// Email/password signup
function signup() {
  firebase.auth().createUserWithEmailAndPassword(email.value, password.value)
    .then((userCredential) => {
      alert("Successfully registered!");
      message.innerText = "Signup successful!";
    })
    .catch((error) => {
      message.innerText = error.message;
    });
}

// Forgot password
function forgotPassword() {
  firebase.auth().sendPasswordResetEmail(email.value)
    .then(() => {
      message.innerText = "Password reset email sent!";
    })
    .catch((error) => {
      message.innerText = error.message;
    });
}

// Gmail login
function loginWithGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  firebase.auth().signInWithPopup(provider)
    .then((result) => {
      const user = result.user;
      alert(`Welcome, ${user.displayName}`);
      message.innerText = `Logged in as ${user.email}`;
    })
    .catch((error) => {
      message.innerText = error.message;
    });
}
