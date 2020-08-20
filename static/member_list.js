import { sendRequest, getGlobal } from "./utils.js";

sendRequest("/members/", new URLSearchParams())
    .then(res => res.json())
    .then(json => {
        let container = document.getElementById("member-id-list");
        json.forEach(member => {
            let elem = document.createElement("div");
            let classAttribute = document.createAttribute("class");
            classAttribute.value = "member-id-list-entry";
            elem.attributes.setNamedItem(classAttribute);
            elem.textContent = member.id;
            container.appendChild(elem);
        });
    });
