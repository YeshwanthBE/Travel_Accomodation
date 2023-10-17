document.addEventListener("DOMContentLoaded", function() {
    var checkinInput = document.getElementById("checkin");
    var checkoutInput = document.getElementById("checkout");   
    var priceDisplay = document.getElementById("price");
    var CGST = document.getElementById("CGST");
    var SGST = document.getElementById("SGST");
    var Totalprice = document.getElementById("Totalprice");
    bdates=JSON.parse(bdates)
    blockeddates=JSON.parse(blockeddates)
    console.log(blockeddates)
    
    
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
    function bdatesfun(element,event){
      var selectedDate = element.value;
      if (bdates.includes(selectedDate)) {
        element.value = ''; // Clear the input
  }
    }
    checkinInput.addEventListener("input",function(event){
      var selectedCheckinDate = new Date(checkinInput.value);
      var selectedCheckoutDate = new Date(checkoutInput.value);
      if(selectedCheckoutDate && selectedCheckinDate>selectedCheckoutDate)
            {checkoutInput.value = "";}
      selectedCheckinDate.setDate(selectedCheckinDate.getDate() + 1);
      checkoutInput.min = selectedCheckinDate.toISOString().split('T')[0];
      bdatesfun(checkinInput,event);

      var selectedCheckinDate = new Date(checkinInput.value);
      nearestBlockedDate = blockeddates.find(function (blockedDate) {
      var checkinDate = new Date(blockedDate.checkin);
      return checkinDate >= selectedCheckinDate;
    });

    if (nearestBlockedDate) {
      checkoutInput.max = nearestBlockedDate.checkin;
    } else {
      checkoutInput.max = ""; // If no blocked date found, clear the max attribute
    }
    })

    checkoutInput.addEventListener("input", function(){
      calculatePrice();
    });
  });
  
