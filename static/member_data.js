let data = JSON.parse(document.getElementById("json-data").textContent);

document.getElementById("member-id").textContent = data.id;
document.getElementById("member-name").textContent = data.name;
document.getElementById("member-email").textContent = data.email;
document.getElementById("member-joined").textContent = data.joined.split(" ")[0];
document.getElementById("member-renewed").textContent = data.renewed.split(" ")[0];
document.getElementById("member-subscribed").textContent = data.subscribed ? "yes" : "no";
