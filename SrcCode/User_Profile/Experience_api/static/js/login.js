document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('form');
    var usernameInput = document.getElementById('mailid');
    var passwordInput = document.getElementById('password');
    var ue =document.getElementById('username-error')
    var pe = document.getElementById('password-error')
    form.addEventListener('submit', function (event) {
      if (usernameInput.value.trim() === '' && passwordInput.value.trim() === '') {
        event.preventDefault();
        ue.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Username is required';
        pe.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Password is required';
        ue.style.opacity=1;
        pe.style.opacity=1;
      }
      if (usernameInput.value.trim() === '') {
        event.preventDefault();
        ue.style.opacity=1;
        ue.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Username is required';
      }
      if (passwordInput.value.trim() === '') {
        event.preventDefault();
        pe.style.opacity=1;
        pe.innerHTML = '<i class="fa fa-exclamation-triangle"></i> Password is required';
      }
    });
    function hideErrorMessage(element, em) {
  element.addEventListener('click', function() {
    em.style.opacity = 0;
    em.style.zIndex=-1
  });
}

hideErrorMessage(usernameInput, ue);
hideErrorMessage(passwordInput, pe);
hideErrorMessage(ue, ue);
hideErrorMessage(pe, pe);

  });
  