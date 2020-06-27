function returnFromLogin() {
    let params = new URLSearchParams(window.location.search);
    if (params.get("return-to") != null) {
        console.log(params.get("return-to"));
        window.location.replace(params.get("return-to"));
    } else {
        window.location.replace("/");
    }
}

function submitPassword() {
    tryLogin(document.getElementById("passwordinput").value);
}

async function tryLogin(password) {
    let statusCode = await fetch("/authorized/", {
        headers: new Headers({
            "Authorization": "Basic " + btoa(":" + password),
             'Content-Type': 'application/x-www-form-urlencoded'
        })
    }).then(resp => resp.status);

    if (statusCode === 200) {
        document.cookie = "auth=" + password + ";max-age=30;path=/";
        returnFromLogin();
    } else {
        document.getElementById("infotext").textContent = "Login failed";
    }
}
