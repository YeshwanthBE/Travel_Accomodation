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
        passwordErrors.style.opacity=0;passwordErrors.style.zIndex=-1;
        if (password !== confirmPassword) {
            cnfpwdErrors.innerHTML = "<i class='fa fa-exclamation-triangle'></i>Passwords do not match!!";
            cnfpwdErrors.style.opacity=1;cnfpwdErrors.style.zIndex=1;
            
        } else {
            cnfpwdErrors.innerHTML = "";
            cnfpwdErrors.style.opacity=0;cnfpwdErrors.style.zIndex=-1;
        }
    });
    passwordInput.addEventListener("input", function () {
        const password = passwordInput.value;
        let errors = ["<i class='fa fa-exclamation-triangle'></i>Must Contain at least &nbsp;"];
        cnfpwdErrors.style.opacity=0;cnfpwdErrors.style.zIndex=-1;
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
            {passwordErrors.style.opacity=0;passwordErrors.style.zIndex=-1;}
        else
            {passwordErrors.style.opacity=1;passwordErrors.style.zIndex=1;}
        passwordErrors.innerHTML = errors.join("");
    });
});