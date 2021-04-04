import { getGlobal, sendRequest } from "./utils.js";

let infoText = document.getElementById("info-text");
let emailInfoText = document.getElementById("email-info-text");

function setInfoText(elem, info) {
    elem.style = "";
    elem.textContent = info;
}

let subjectField    = document.getElementById("subject-input");
let receiversField  = document.getElementById("receivers-input");
let templateField   = document.getElementById("template-input");

receiversField.onchange = async function() {
    let params = new URLSearchParams();
    params.append("receivers", receiversField.value);

    sendRequest("/email_list/", params)
        .then(resp => resp.json())
        .then(receivers => {
            // This check might be unnecessary
            if (receivers.length > 0) {
                let p = receivers.length === 1 ? "person" : "people";
                setInfoText(emailInfoText, `${receivers.length} ${p} will be emailed`)
            } else {
                emailInfoText.style = "display: none;";
            }
        })
        .catch(error => setInfoText(infoText, error));
}

getGlobal().submit = function() {

    if (!confirm("Really send emails?")) {
        return;
    }

    let subject    = subjectField.value;
    let receivers  = receiversField.value;
    let template   = templateField.value;

    let params = new URLSearchParams();
    params.append("subject", subject);
    params.append("receivers", receivers);
    params.append("template", template);

    if (subject === "" || receivers === "" || template === "") {
        setInfoText(infoText, "All fields are required");
        return;
    }

    infoText.style = "display: none;";
    emailInfoText.style = "display: none;";

    sendRequest("/email_members/", params)
        .then(resp => {
            if (resp.status === 200) {
                subjectField.value = "";
                receiversField.value = "";
                templateField.value = "";
            }
            return resp.text()
        })
        .then(text => setInfoText(infoText, text))
        .catch(error => setInfoText(infoText, error));
}
