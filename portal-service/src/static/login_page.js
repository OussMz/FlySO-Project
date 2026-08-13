const loginChoiceBtn = document.querySelector("#login-choice-btn");
const registerChoiceBtn = document.querySelector("#register-choice-btn");
const loginContainer = document.querySelector("#login-form-container");
const registerContainer = document.querySelector("#register-form-container");

const signinBtn = document.querySelector("#sign-in-btn");
const signupBtn = document.querySelector("#sign-up-btn");


displayed = "login"

loginChoiceBtn.addEventListener("click", ()=> {
    if (displayed == "login") return;

    registerContainer.classList.remove("active");
    loginContainer.classList.add("active");

    displayed = "login";
});

registerChoiceBtn.addEventListener("click", ()=> {
    if (displayed == "register") return;

    loginContainer.classList.remove("active");
    registerContainer.classList.add("active");

    displayed = "register";

});

const signinHiddenMessage = document.querySelector("#sign-in-hidden-msg");
const signupHiddenMessage = document.querySelector("#sign-up-hidden-msg");

function displayMessage(hiddenMessage, status, message){
    let toRemove;
    let toAdd;
    
    if (status == "success"){
        toRemove = "error";
        toAdd = "success";
    }
    else{
        toRemove = "success";
        toAdd = "error";
    }

    hiddenMessage.classList.remove(toRemove);
    hiddenMessage.classList.add(toAdd);
    hiddenMessage.innerHTML = message;
    hiddenMessage.style.display = "block";
}

signupBtn.addEventListener("click", async (e)=> {
    e.preventDefault();
    
    const theUsername = document.querySelector("#register-username").value;
    const theEmail = document.querySelector("#register-email").value;
    const thePassword = document.querySelector("#register-password").value;
    const thePasswordRepeated = document.querySelector("#register-confirm-password").value;


    if (thePassword != thePasswordRepeated) {
        displayMessage(signupHiddenMessage, "error", "The entered passwords don't match.");
        return
    };

    data = {
        "username": theUsername,
        "email": theEmail,
        "password": thePassword,
        "repeatedPassword": thePasswordRepeated,
    }

    const response = await fetch("/signup", {
        method: "POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify(data)
    });
    
    const responseBody = await response.json();
    message = responseBody["message"];

    if (response.ok){
        displayMessage(signupHiddenMessage, "success", message);
    }
    else {
        displayMessage(signupHiddenMessage, "error", message);
    }
});

signinBtn.addEventListener("click", async (e)=> {
    e.preventDefault();
    
    const theEmail = document.querySelector("#login-email").value;
    const thePassword = document.querySelector("#login-password").value;

    data = {
        "email": theEmail,
        "password": thePassword,
    }

    const response = await fetch("/signin", {
        method: "POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify(data)
    });

    const responseBody = await response.json();
    message = responseBody["message"];

    if (response.ok){
        window.location.href = "/";
    }
    else {
        displayMessage(signinHiddenMessage, "error", message);
    }
});