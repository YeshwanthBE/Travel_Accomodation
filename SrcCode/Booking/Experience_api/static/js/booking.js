document.addEventListener("DOMContentLoaded", function() {
    var checkinInput = document.getElementById("checkin");
   
  
    function disableDates(event) {
      var selectedDate = new Date(event.target.value);
      console.log(typeof blockedDates)
      if (blockedDates.includes(selectedDate.toISOString().split('T')[0])) {
        event.target.setCustomValidity("This date is blocked.");
      } else {
        event.target.setCustomValidity("");
      }
    }
  
    checkinInput.addEventListener("input", disableDates);
  });
  
