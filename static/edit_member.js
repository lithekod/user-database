import { sendRequest } from "./utils.js";

let idField         = document.getElementById("id-input");
let nameField       = document.getElementById("name-input");
let emailField      = document.getElementById("email-input");
let joinedField     = document.getElementById("joined-input");
let renewedField    = document.getElementById("renewed-input");
let subscribedField = document.getElementById("subscribed-input");

sendRequest("/members/", new URLSearchParams([["id", member_id]]))
    .then(res => res.json())
    .then(json => {
        idField.textContent = json.id;
        nameField.value = json.name;
        emailField.value = json.email;
        joinedField.value = json.joined.split(" ")[0];
        renewedField.value = json.renewed.split(" ")[0];
        subscribedField.textContent = json.receive_email === 1 ? "yes" : "no";

        let linkList = document.getElementById("link-list");
        Object.entries(json.links).forEach(elem => {
            let [key, value] = elem;
            let entry = document.createElement("li");
            entry.innerHTML = "<a href=\"/" + value + "\">" + key + "</a>";
            linkList.appendChild(entry);
        });
    });

function setInfoText(info) {
    let elem = document.getElementById("info-text");
    elem.style = "";
    elem.textContent = info;
}

function changeField(field, value, onsuccess=function(){}) {
    let params = new URLSearchParams();
    params.append("id", member_id);
    params.append("field", field);
    params.append("new", value);

    sendRequest("/modify/", params)
        .then(resp => {
            if (resp.status === 200) {
                onsuccess();
            }
            return resp.text();
        })
        .then(text => setInfoText(text))
        .catch(error => setInfoText(error));
}

subscribedField.onclick = function() {
    if (subscribedField.textContent === "no") {
        changeField("receive_email", "1", () => subscribedField.textContent = "yes");
    } else {
        changeField("receive_email", "0", () => subscribedField.textContent = "no");
    }

    return false;
};

nameField.onchange = function() {
    changeField("name", nameField.value);
}

emailField.onchange = function() {
    changeField("email", emailField.value);
}

joinedField.onchange = function() {
    changeField("joined", joinedField.value);
}

renewedField.onchange = function() {
    changeField("renewed", renewedField.value);
}
