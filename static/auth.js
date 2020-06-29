import { getCookie } from "./utils.js";

if (getCookie("auth") === "") {
    let path = encodeURIComponent(window.location.pathname);
    let loginPage = "/gui/login/?return-to=" + path;
    window.location.replace(loginPage);
}
