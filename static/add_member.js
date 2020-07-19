import { getCookie, getGlobal } from "./utils.js";

function sendRequest(endpoint, parameters) {
    let bearer = getCookie("auth");
    return fetch(endpoint + "?" + parameters.toString(), {
        headers: new Headers({
            "Authorization": "Bearer " + bearer,
             'Content-Type': 'application/x-www-form-urlencoded'
        })
    })
}

function setInfoText(info) {
    let elem = document.getElementById("info-text");
    elem.style = "";
    elem.textContent = info;
}

let emailFieldEdited = false;
let idField    = document.getElementById("id-input");
let nameField  = document.getElementById("name-input");
let emailField = document.getElementById("email-input");


getGlobal().submit = function() {
    let id    = idField.value;
    let name  = nameField.value;
    let email = emailField.value;

    let params = new URLSearchParams();
    params.append("id", id);
    params.append("name", name);
    params.append("email", email);

    let infoElem = document.getElementById("info-text");
    infoElem.style = "display: none;";

    if (id === "" || name === "" || email === "") {
        setInfoText("All fields are required");
        return;
    }

    sendRequest("/add_member/", params)
        .then(resp => {
            if (resp.status === 200) {
                idField.value = "";
                nameField.value = "";
                emailField.value = "";
                emailFieldEdited = false;
            }
            return resp.text()
        })
        .then(text => setInfoText(text))
        .catch(error => setInfoText(error));
}

idField.oninput = function() {
    if (emailFieldEdited) {
        return;
    }

    if (idField.value !== "") {
        emailField.value = idField.value + "@student.liu.se";
    } else {
        emailField.value = "";
    }
}

emailField.oninput = function() {
    emailFieldEdited = emailField.value !== "";
};
