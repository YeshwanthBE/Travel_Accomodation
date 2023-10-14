document.addEventListener("DOMContentLoaded", function () {
    var usernameInput = document.getElementById('mailid');
    const passwordInput = document.getElementById("password");
    const passwordErrors = document.getElementById("password-errors");
    const cnfpwdip= document.getElementById("confirm_password");
    const cnfpwdErrors = document.getElementById("cnfpwd-errors");
    const nameInput = document.getElementById("name");
    const submit = document.getElementById("submit");
    const phno = document.getElementById("phno");
    var ue =document.getElementById('username-error')
    var ne =document.getElementById('name-error')
    var pe=document.getElementById('phno-error')
    submitbutton=true;
    phno.addEventListener("input", function () {
        let ph = phno.value;
    ph = ph.replace(/\D/g, '');
    if (!/^[6-9]/.test(ph)) {
        ph = ph.substring(1);
    }
    phno.value = ph;
    }); 
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
            togglevisiblity(cnfpwdErrors,true);
            submitbutton=false;        
        } else {
            cnfpwdErrors.innerHTML = "";
            togglevisiblity(cnfpwdErrors,false);
        }
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
        if(errors.length>1)
            {togglevisiblity(passwordErrors,true);submitbutton=false;}
        passwordErrors.innerHTML = errors.join("");
    });
    function togglevisiblity(element,flag){
        console.log("toggles")
        if(flag){element.style.opacity=1;
        element.style.zIndex=1;
        setTimeout(function () {
            togglevisiblity(element,false);
        }, 2000);
    }
        else{element.style.opacity=0;
            element.style.zIndex=-1;
        }
    }
    submit.addEventListener("click",function(event){
        passwordInput.dispatchEvent(new Event("input"));
        cnfpwdip.dispatchEvent(new Event("input"));
        flag=true;
        if (usernameInput.value.trim() === '') {
            togglevisiblity(ue,true);
            ue.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Mailid is required';
            flag=false;
          }
          if (nameInput.value.trim() === '') {
            togglevisiblity(ne,true);
            ne.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Username is required';
            flag=false;
          }
          if (phno.value.trim() === '') {
            togglevisiblity(pe,true);
            pe.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Phone No is required';
            flag=false;
          }
        if (!submitbutton) {
            togglevisiblity(passwordErrors,true);
            flag=false;
        }

        if(!flag){
            event.preventDefault();
        }
    usernameInput.addEventListener("click",function(){
        togglevisiblity(ue,false);
    });
    nameInput.addEventListener("click",function(){
        togglevisiblity(ne,false);
    });
    phno.addEventListener("click",function(){
        togglevisiblity(pe,false);
    });
    });
    const sd = JSON.parse(sdjson).states;
    const stateDropdown = document.getElementById('stateDropdown');
    const districtDropdown = document.getElementById('districtDropdown');
    function populateStateDropdown() {
        for (const state of sd) {
            const option = document.createElement('option');
            option.value = state.state;
            option.text = state.state;
            stateDropdown.appendChild(option);
      }
    }
    function populateDistrictDropdown() {
        const selectedState = stateDropdown.value;
        const selectedStateData = sd.find(stateData => stateData.state === selectedState);
        districtDropdown.innerHTML = '';
        const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.text = 'Select a district';
    districtDropdown.appendChild(defaultOption);
        if (selectedStateData) {
            for (const district of selectedStateData.districts) {
                const option = document.createElement('option');
                option.value = district;
                option.text = district;
                districtDropdown.appendChild(option);
            }
        }
    }
    document.getElementById('stateDropdown').addEventListener('change', populateDistrictDropdown); 
      populateStateDropdown();
});

