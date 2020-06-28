async function submitPassword() {
    let infoText = document.getElementById("info-text");
    infoText.style = "display: none;";

    let loggedIn = await tryLogin(document.getElementById("passwordinput").value);

    if (!loggedIn) {
        infoText.style = "margin-top: 0.5em; margin-bottom: 0;";
    }
}

function handleKeyPress(e) {
    if (e.key === "Enter") {
        submitPassword();
    }
}

function returnFromLogin() {
    let params = new URLSearchParams(window.location.search);
    if (params.get("return-to") != null) {
        console.log(params.get("return-to"));
        window.location.replace(params.get("return-to"));
    } else {
        window.location.replace("/");
    }
}

async function tryLogin(password) {
    let statusCode = await fetch("/authorized/", {
        headers: new Headers({
            "Authorization": "Basic " + btoa(":" + password),
             'Content-Type': 'application/x-www-form-urlencoded'
        })
    }).then(resp => resp.status);

    if (statusCode === 200) {
        document.cookie = "auth=" + password + ";max-age=21600;path=/";
        returnFromLogin();
        return true;
    }

    return false;
}
