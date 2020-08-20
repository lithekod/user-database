export function getCookie(cname) {
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

export function getGlobal() {
    return window;
}

export function sendRequest(endpoint, parameters) {
    let bearer = getCookie("auth");
    return fetch(endpoint + "?" + parameters.toString(), {
        headers: new Headers({
            "Authorization": "Bearer " + bearer,
             'Content-Type': 'application/x-www-form-urlencoded'
        })
    })
}
