let active = document.getElementById("active-members");
let total  = document.getElementById("total-members");

fetch("/member_count/")
    .then(res => res.json())
    .then(json => {
        active.textContent = json.active_members;
        total.textContent  = json.total_members;
    });
