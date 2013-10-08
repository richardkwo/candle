$(function() {
  $('.menu a').click(function(ev) {
    ev.preventDefault();
    var selected = 'selected';

    $('.mainview > *').removeClass(selected);
    $('.menu li').removeClass(selected);
    setTimeout(function() {
      $('.mainview > *:not(.selected)').css('display', 'none');
    }, 100);

    $(ev.currentTarget).parent().addClass(selected);
    var currentView = $($(ev.currentTarget).attr('href'));
    currentView.css('display', 'block');
    setTimeout(function() {
      currentView.addClass(selected);
    }, 0);

    setTimeout(function() {
      $('body')[0].scrollTop = 0;
    }, 200);
  });

  $('.mainview > *:not(.selected)').css('display', 'none');

  $('#server').val(localStorage.server);

  var to_email = localStorage.to_email;
  if (to_email) {
      var splitter = to_email.split('@');
      if (splitter.length > 1 ) {
        $('#kindle-email-name').val(splitter[0]);
        $('#kindle-email-domain').val(splitter[1]);
      }
  }

  $('#save-btn').click(function(){
    localStorage.server = $('#server').val();
    localStorage.to_email = $('#kindle-email-name').val() + 
        '@' + $('#kindle-email-domain').val();
    $('#saved-tip').fadeIn(500).fadeOut(500);
  });
});
