document.addEventListener("DOMContentLoaded", function () {
    var usernameInput = document.getElementById('mailid');
    const nameInput = document.getElementById("name");
    const submit = document.getElementById("submit");
    const phno = document.getElementById("phno");
    const desc=document.getElementById("description");
    const address=document.getElementById("address")
    const image=document.getElementById("image");
    const price=document.getElementById("price");
    var ue =document.getElementById('username-error')
    var ne =document.getElementById('name-error')
    var pe=document.getElementById('phno-error')
    var ae =document.getElementById('address-error')
    var de =document.getElementById('desc-error')
    var ie=document.getElementById('image-error')
    var pre=document.getElementById('price-error')
    submitbutton=true;
    cnfbutton=true;
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
        name = name.replace(/[^A-Za-z\s]/g, '');
        nameInput.value = name;
    });
    function togglevisiblity(element,flag){
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
          if (address.value.trim() === '') {
            togglevisiblity(ae,true);
            ae.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Address is required';
            flag=false;
          }
          if (desc.value.trim() === '') {
            togglevisiblity(de,true);
            de.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Description is required';
            flag=false;
          }
          if (image.value.trim() === '') {
            togglevisiblity(ie,true);
            ie.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Image is required';
            flag=false;
          }
          if (price.value === '') {
            togglevisiblity(pre,true);
            pre.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Price is required';
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

