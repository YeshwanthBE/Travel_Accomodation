document.addEventListener("DOMContentLoaded", function () {
    const modifyButton = document.getElementById("modifyButton");
    const nameSpan = document.getElementById("name");
    const addressSpan = document.getElementById("address");
    const phnoSpan = document.getElementById("phno");
    const price = document.getElementById("price");
    const description = document.getElementById("description");
    const saveButton = document.getElementById("savebutton");
    const img=document.getElementById("acmimg");
    const imgform=document.getElementById("image-upload-form");
    const imageFileInput = document.getElementById("image-file");
    const delcon = document.getElementById("delcon");
    const labelElement = document.querySelector('label.button[for="image-file"]');
    function initialize(){
        nsc=nameSpan.textContent
        asc=addressSpan.textContent
        psc=phnoSpan.textContent
        dsc=description.textContent
        prsc=price.textContent
        img.style.display="block";
        imgform.style.display="none";
        delcon.style.display="none";
    }
    function toggledisplay(element){
        element.style.display=element.style.display==="block"?"none":"block";
    }
    imageFileInput.addEventListener("change", function () {
        if (imageFileInput.files.length > 0) {
            labelElement.innerHTML=imageFileInput.files[0].name;
            toggledisplay(delcon);
        }
    });
    delcon.addEventListener("click",function(){
        imageFileInput.value="";
        labelElement.innerHTML="Upload";
        toggledisplay(delcon);
    });
    function toggleContentAndVisibility() {
        toggleContentEditable(nameSpan,nsc);
        toggleContentEditable(addressSpan,asc);
        toggleContentEditable(phnoSpan,psc);
        toggleContentEditable(description,dsc);
        toggleContentEditable(price,prsc);
        toggleVisibility(saveButton);
        toggledisplay(img);
        toggledisplay(imgform);
        modifyButton.innerHTML=modifyButton.innerHTML==="Modify"?"Back":"Modify";
    }

    modifyButton.addEventListener("click", toggleContentAndVisibility);

    function toggleContentEditable(element,originalvalue) {
        element.contentEditable = element.contentEditable === "true" ? "false" : "true";
        element.classList.toggle("modify");
        element.textContent = originalvalue;
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
        initialize();
    });
    function getcontent(element){
        element.contentEditable="false";
        return element.textContent;
    }
    initialize();
});