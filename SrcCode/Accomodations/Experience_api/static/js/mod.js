document.addEventListener("DOMContentLoaded", function () {
    const modifyButton = document.getElementById("modifyButton");
    const nameSpan = document.getElementById("name");
    const addressSpan = document.getElementById("address");
    const phnoSpan = document.getElementById("phno");
    const saveButton = document.getElementById("savebutton");
    const pfButtons = document.querySelector(".pfbuttons");
    function toggleContentAndVisibility() {
        toggleContentEditable(nameSpan);
        toggleContentEditable(addressSpan);
        toggleContentEditable(phnoSpan);
        toggleVisibility(saveButton);
    }

    modifyButton.addEventListener("click", toggleContentAndVisibility);

    function toggleContentEditable(element) {
        element.contentEditable = element.contentEditable === "true" ? "false" : "true";
        element.classList.toggle("modify");
    }
    function toggleVisibility(element) {
        element.style.visibility = element.style.visibility === "visible" ? "hidden" : "visible";
        pfButtons.style.height = pfButtons.style.height === "112px"? "56px" :" 112px";
    }
    saveButton.addEventListener("click", function() {
        modifiedname=getcontent(nameSpan)
        modiifiedaddress=getcontent(addressSpan)
        modifiedphno=getcontent(phnoSpan)
        const data = {
            name: modifiedname,
            address: modiifiedaddress,
            phno: modifiedphno
        };
        var modUrl = document.getElementById('savebutton').getAttribute('data-mod-url');
        $.ajax({
            url: modUrl, // Replace with the correct URL
            method: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
                console.log(response);
            }
        });
        toggleContentAndVisibility();
    });
    function getcontent(element){
        element.contentEditable="false";
        return element.textContent;
    }
});