document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("password");
    const passwordErrors = document.getElementById("password-errors");
    const cnfpwdip= document.getElementById("confirm_password");
    const cnfpwdErrors = document.getElementById("cnfpwd-errors");
    const nameInput = document.getElementById("name");

    nameInput.addEventListener("input", function () {
        let name = nameInput.value;
        name = name.replace(/[^A-Za-z]/g, '');

        nameInput.value = name;
    });

    cnfpwdip.addEventListener("input", function () {
        const password = passwordInput.value;
        const confirmPassword = cnfpwdip.value;
        togglevisiblity(passwordErrors,false)
        if (password !== confirmPassword) {
            cnfpwdErrors.innerHTML = "<i class='fa fa-exclamation-triangle'></i>Passwords do not match!!";
            togglevisiblity(cnfpwdErrors,true)
            
        } else {
            cnfpwdErrors.innerHTML = "";
            togglevisiblity(cnfpwdErrors,false)
        }
        setTimeout(function () {
            togglevisiblity(cnfpwdErrors,false);
        }, 5000);
    });
    passwordInput.addEventListener("input", function () {
        const password = passwordInput.value;
        let errors = ["<i class='fa fa-exclamation-triangle'></i>Must Contain at least &nbsp;"];
        togglevisiblity(cnfpwdErrors,false)
        if (password.length < 8) {
            errors.push("<pre>     &bull; 8 characters.</pre>");
        }

        if (!/[A-Z]/.test(password) ) {
            errors.push("<pre>     &bull; one uppercase letter</pre>");
        }
        if (!/\d/.test(password) ) {
            errors.push("<pre>     &bull; one number</pre>");
        }
        if (!/[!@#$%^&*]/.test(password)) {
            errors.push("<pre>     &bull; one symbol.</pre>");
        }
        const userName =nameInput.value;

        if (password.includes(userName)) {
            errors.push("<i class='fa fa-exclamation-triangle'></i>Password should not contain your username.</pre>");
        }
        if(errors.length===1)
            {togglevisiblity(passwordErrors,false)}
        else
            {togglevisiblity(passwordErrors,true)}
        passwordErrors.innerHTML = errors.join("");
        setTimeout(function () {
            togglevisiblity(passwordErrors,false);
        }, 5000);
    });
    function togglevisiblity(element,flag){
        if(flag){element.style.opacity=1;
        element.style.zIndex=1;}
        else{element.style.opacity=0;
            element.style.zIndex=-1;
        submitbutton=flag;
        }
    }
});