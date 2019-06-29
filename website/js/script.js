
$(document).ready(function(){
    $('.slideshow').slick({
        adaptiveHeight: true,
        arrows: true,
        
    });

    $('.galleryslide').slick({
    adaptiveHeight:true,
        slidesToShow: 5,
        autoplay: true,
        autoplaySpeed: 2000,
        responsive: [
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                }

            },
            {
                breakpoint: 1025,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 4
                }
            },
            {
                breakpoint: 800,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3
                }
            }
            
        ]
    });

   
  });

function gotodiscord() {
    location.replace("https://discordapp.com/api/oauth2/authorize?client_id=525814724567367682&redirect_uri=http%3A%2F%2Flocalhost%2FRAM%2Fdashboard.html&response_type=token&scope=identify%20guilds")

}
function dropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  window.onclick = function(event) {
    if (!event.target.matches('.dropdown')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  } 
 