import { getGlobal, sendRequest } from "./utils.js";

function setInfoText(info) {
    let elem = document.getElementById("info-text");
    elem.style = "";
    elem.textContent = info;
}

let subjectField    = document.getElementById("subject-input");
let receiversField  = document.getElementById("receivers-input");
let templateField   = document.getElementById("template-input");


getGlobal().submit = function() {
    let subject    = subjectField.value;
    let receivers  = receiversField.value;
    let template   = templateField.value;

    let params = new URLSearchParams();
    params.append("subject", subject);
    params.append("receivers", receivers);
    params.append("template", template);

    let infoElem = document.getElementById("info-text");
    infoElem.style = "display: none;";

    if (subject === "" || receivers === "" || template === "") {
        setInfoText("All fields are required");
        return;
    }

    sendRequest("/email_members/", params)
        .then(resp => {
            if (resp.status === 200) {
                subjectField.value = "";
                receiversField.value = "";
                templateField.value = "";
            }
            return resp.text()
        })
        .then(text => setInfoText(text))
        .catch(error => setInfoText(error));
}
