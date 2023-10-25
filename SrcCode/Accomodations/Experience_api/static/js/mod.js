document.addEventListener("DOMContentLoaded", function () {
    const modifyButton = document.getElementById("modifyButton");
    const nameSpan = document.getElementById("name");
    const addressSpan = document.getElementById("address");
    const phnoSpan = document.getElementById("phno");
    const price = document.getElementById("price");
    const description = document.getElementById("description");
    const saveButton = document.getElementById("savebutton");
    function toggleContentAndVisibility() {
        toggleContentEditable(nameSpan);
        toggleContentEditable(addressSpan);
        toggleContentEditable(phnoSpan);
        toggleContentEditable(description);
        toggleContentEditable(price);
        toggleVisibility(saveButton);
    }

    modifyButton.addEventListener("click", toggleContentAndVisibility);

    function toggleContentEditable(element) {
        element.contentEditable = element.contentEditable === "true" ? "false" : "true";
        element.classList.toggle("modify");
        
    }
    function toggleVisibility(element) {
        element.style.visibility = element.style.visibility === "visible" ? "hidden" : "visible";
    }
    saveButton.addEventListener("click", function() {
        modifiedname=getcontent(nameSpan)
        modiifiedaddress=getcontent(addressSpan)
        modifiedphno=getcontent(phnoSpan)
        modifiedprice=getcontent(price)
        modifieddesc=getcontent(description)
        const data = {
            name: modifiedname,
            location: modiifiedaddress,
            phno: modifiedphno,
            price: modifiedprice,
            description: modifieddesc
        };
        var modUrl = document.getElementById('savebutton').getAttribute('data-mod-url');
        $.ajax({
            url: modUrl, // Replace with the correct URL
            method: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
            }
        });
        toggleContentAndVisibility();
    });
    function getcontent(element){
        element.contentEditable="false";
        return element.textContent;
    }
});