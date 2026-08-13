const submissionBtn = document.querySelector("#submission-btn");

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

submissionBtn.addEventListener("click", async (e)=>{
    e.preventDefault();

    const fullName = document.querySelector("#full-name").value;
    const email = document.querySelector("#email").value;
    const age = document.querySelector("#age").value;
    const medicalCertificate = document.querySelector("#medical-certificate").value;
    const gpa = document.querySelector("#gpa").value;
    const flightHours = document.querySelector("#flight-hours").value;
    
    const hiddenMessage = document.querySelector("#hidden-msg");
    
    if (gpa<0 || gpa>4){
        displayMessage(hiddenMessage, "error", "GPA must be betxeen 0 and 4.");
        return
    }

    data = {
        "full_name": fullName,
        "email": email,
        "age": age,
        "medical_certificate": medicalCertificate,
        "gpa": gpa,
        "flight_hours": flightHours
    }
    

    for (const val of Object.values(data)){
        if (val == ""){
        displayMessage(hiddenMessage, "error", "All fields are required. Make sure to fill them all.");
        return
        }
    }


    const response = await fetch("/api/apply", {
        method: "POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify(data)
    });

    const responseBody = await response.json();

    const message = responseBody["message"];

    if (response.ok){
        displayMessage(hiddenMessage, "success", message);
    }
    else {
        displayMessage(hiddenMessage, "error", message);
    }


});