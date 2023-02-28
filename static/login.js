function returnFromLogin() {
    let params = new URLSearchParams(window.location.search);
    if (params.get("return-to") != null) {
        console.log(params.get("return-to"));
        window.location.replace(params.get("return-to"));
    } else {
        window.location.replace("/");
    }
}

function onSignIn(credentialResponse) {
    fetch("/login/", {
        method: "POST",
        headers: new Headers({
            "Accept": "application/json, text/plain, */*",
            "Content-Type": 'application/json'
        }),
        body: JSON.stringify({ token: credentialResponse.credential })
    })
        .then(resp => resp.text())
        .then(text => {
            if (resp.status === 401) {
                let infoText = document.getElementById("info-text");
                infoText.style = "";
                infoText.textContent = text;
                gapi.auth2.getAuthInstance().signOut();
            } else if (resp.status === 200) {
                returnFromLogin();
            }
        });
}
