const logoutLink = document.querySelector("#logout-link");

if (logoutLink){
    logoutLink.addEventListener("click", async (e)=>{
        e.preventDefault();
    
        const response = await fetch("/logout", {
            method: "POST"
        });

        window.location.href = "/";
    });
}