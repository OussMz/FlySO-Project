const applicationsTableBody = document.querySelector("#applications-table-body");

applicationsTableBody.addEventListener("click", async (event) =>{
    if (event.target.classList.contains("btn-accept") ||
        event.target.classList.contains("btn-reject")) {
            
            const pressedBtn = event.target;
            const applicationId = pressedBtn.dataset.appId;
            const relevantRow = pressedBtn.closest("tr");

            let action;
            if (pressedBtn.classList.contains("btn-accept")) action = "accept";
            else action = "reject";

            const newStatus = `${action}ed`;

            payload = {
                "id": applicationId,
                "status": newStatus
            }
            
            relevantRow.innerHTML = `<td colspan="8">
            <div class="action-message ${action}">
            The application was successfully ${action}ed.
            </div>
            </td>`;
            
            setTimeout(()=>{
                relevantRow.remove();
            }, 3000)
            
            const response = await fetch("/update-status", {
                method: "PUT",
                headers: {"content-type": "application/json"},
                body: JSON.stringify(payload)
            });
    }
});