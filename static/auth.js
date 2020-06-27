if (document.cookie === "") {
    let path = encodeURIComponent(window.location.pathname);
    let loginPage = "/gui/login/?return-to=" + path;
    window.location.replace(loginPage);
}
