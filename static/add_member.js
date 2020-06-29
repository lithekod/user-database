function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }

    return "";
}

function sendRequest(endpoint, parameters) {
    let password = getCookie("auth");
    return fetch(endpoint + "?" + parameters.toString(), {
        headers: new Headers({
            "Authorization": "Basic " + btoa(":" + password),
             'Content-Type': 'application/x-www-form-urlencoded'
        })
    })
}

function submit() {
    let id    = document.getElementById("id-input").value;
    let name  = document.getElementById("name-input").value;
    let email = document.getElementById("email-input").value;

    let params = new URLSearchParams();
    params.append("id", id);
    params.append("name", name);
    params.append("email", email);

    let infoElem = document.getElementById("info-text");
    infoElem.style = "display: none;";

    if (id === "" || name === "" || email === "") {
        infoElem.style = "";
        infoElem.textContent = "All fields are required";
        return;
    }

    sendRequest("/add_member/", params)
        .then(resp => resp.text())
        .then(text => {
            infoElem.style = "";
            infoElem.textContent = text;
        })
        .catch(error => {
            infoElem.style = "";
            infoElem.textContent = error;
        });
}

function setDefaultEmail() {
    let idField    = document.getElementById("id-input");
    let emailField = document.getElementById("email-input");

    if (idField.value === "" || emailField.value !== "") {
        return;
    }

    emailField.value = idField.value + "@student.liu.se";
}

function setInfoText(info) {
    let elem = document.getElementById("info-text");
    elem.style = "";
    elem.textContent = info;
}
