$(document).ready(function() {
  $(window).scroll(function() {
    if ($(document).scrollTop() > 80) {
      $('.navbar').addClass('affix');
    } else {
      $('.navbar').removeClass('affix');
    }
  });
});
