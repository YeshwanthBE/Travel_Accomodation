document.addEventListener("DOMContentLoaded", function() {
    var checkinInput = document.getElementById("checkin");
    var checkoutInput = document.getElementById("checkout");   
    var priceDisplay = document.getElementById("price");
    var CGST = document.getElementById("CGST");
    var SGST = document.getElementById("SGST");
    var Totalprice = document.getElementById("Totalprice");

    function disableDates(event) {
      var selectedCheckinDate = new Date(checkinInput.value);
      var selectedCheckoutDate = new Date(checkoutInput.value);
      var today = new Date();
      console.log(selectedCheckinDate)
      console.log(selectedCheckoutDate)
      if (selectedCheckinDate < today) {
          checkinInput.setCustomValidity("Check-in date cannot be in the past.");
      } else {
          checkinInput.setCustomValidity("");
      }

      if (selectedCheckoutDate > selectedCheckinDate) {
          ;
      } else {
        checkoutInput.setCustomValidity("Checkout date must be later than the check-in date.");

        // Automatically adjust checkout date to be one day later than check-in date
        var newCheckoutDate = new Date(selectedCheckinDate);
        newCheckoutDate.setDate(newCheckoutDate.getDate() + 1);

        // Update the value and the min attribute of the checkout input
        checkoutInput.value = "";
        checkoutInput.min = newCheckoutDate.toISOString().split('T')[0];
      }
  }
    
    function calculatePrice() {
      var checkinDate = new Date(checkinInput.value);
      var checkoutDate = new Date(checkoutInput.value);

      if (!isNaN(checkinDate.getTime()) && !isNaN(checkoutDate.getTime())) {
          var nights = Math.floor((checkoutDate - checkinDate) / (1000 * 60 * 60 * 24));
          var totalPrice = nights * pricePerNight;
          var GST=0.18*totalPrice;
          priceDisplay.textContent =totalPrice+"₹";
          SGST.textContent=GST+"₹";
          CGST.textContent=GST+"₹";
          Totalprice.textContent=totalPrice+GST*2+"₹";
      } 
      document.getElementById("bill").style.opacity=1;
    }

    checkinInput.addEventListener("input",disableDates)

    checkoutInput.addEventListener("input", function(){
      disableDates();
      calculatePrice();
    });
  });
  
