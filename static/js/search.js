$(document).ready(function() {
  
  var $search = $(".search"),
      $input = $(".search-input"),
      $close = $(".search-close"),
      $svg = $(".search-svg"),
      $path = $(".search-svg__path")[0],
      initD = $svg.data("init"),
      midD = $svg.data("mid"),
      finalD = $svg.data("active"),
      backDelay = 400,
      midAnim = 200,
      bigAnim = 400,
      animating = false;
  
  $(document).on("click", ".search:not(.active)", function() {
    if (animating) return;
    animating = true;
    $search.addClass("active");
    
    Snap($path).animate({"path": midD}, midAnim, mina.backin, function() {
      Snap($path).animate({"path": finalD}, bigAnim, mina.easeinout, function() {
        $input.addClass("visible");
        $input.focus();
        $close.addClass("visible");
        animating = false;
      });
    });
    
  });

  
  $(document).on("click", ".search-close", function() {
    if (animating) return;
    animating = true;
    $input.removeClass("visible");
    $close.removeClass("visible");
    $search.removeClass("active");
    
    setTimeout(function() {
      Snap($path).animate({"path": midD}, bigAnim, mina.easeinout, function() {
        Snap($path).animate({"path": initD}, midAnim, mina.easeinout, function() {
          animating = false;
        });
      });
    }, backDelay);
  });
  


  $(".search-input").on("keydown",function search(e) {
      if(e.keyCode == 13) {
          e.preventDefault();
          var myURL = document.location.href;
          document.location.href = myURL + e.target.value;
          $.busyLoadFull("show");

      }
  });

});