document.addEventListener("DOMContentLoaded", function() {
    var namecard = document.querySelector(".namecard");
    var profilePhoto = document.querySelector(".profile-photo");
    var name = document.querySelector(".name");
    var iconContainer = document.querySelector(".icon-container");
    var imgMe = document.querySelector(".img-me");
    var wholePage = document.querySelector(".whole-page");
    namecard.addEventListener("click", function() {
      namecard.style.boxShadow = "5px 5px 5px 0 lightblue";
      setTimeout(function () {
    namecard.style.boxShadow = "none";
    }, 100);
    })        
  })