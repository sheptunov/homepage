$(function(){
	
	/* Auto clear fields
	-----------------------------------------------------------------------------*/
	$.fn.autoClear = function () {
        $(this).each(function() {
            $(this).data("autoclear", $(this).attr("value"));
        });
        $(this)
            .bind('focus', function() {
                if ($(this).attr("value") == $(this).data("autoclear")) {
                    $(this).attr("value", "").addClass('autoclear-normalcolor');
                }
            })
            .bind('blur', function() {
                if ($(this).attr("value") == "") {
                    $(this).attr("value", $(this).data("autoclear")).removeClass('autoclear-normalcolor');
                }
            });
        return $(this);
    }
 
	$('input[type=text]').autoClear();
	

	/* CSS3 IE fix
	-----------------------------------------------------------------------------*/
	if(window.PIE){
        $('.pie, .items-list li').each(function(){
            PIE.attach(this);
        });
    }
	
	
	/* Selects
	-----------------------------------------------------------------------------*/
	$('.skinned-select').select_skin();
	
	
	
	/* Show popup cart
	-----------------------------------------------------------------------------*/
	$('#showCart').click(function() {
		if ($('#cartPopup').is(':hidden')) $('#cartPopup').fadeIn("fast");
		else $('#cartPopup').fadeOut("fast");
	});

	$(document).bind('click', function(e) {
		var $clicked = $(e.target);
		if (! $clicked.parents().hasClass("cart-popup")) $('#cartPopup').fadeOut("fast");
	});

	/* Show popup login
	-----------------------------------------------------------------------------*/
	$('#showLogin').click(function(){
		$('body').append('<div id="grey-cover"></div>');
		$('#loginPopupBlock').fadeIn('fast');
    });
	$('#grey-cover').live('click', function(){
		$('#loginPopupBlock').fadeOut('fast'); $(this).remove();
    });
	$('#loginPopupBlock .close').live('click', function(){
		$('#loginPopupBlock').fadeOut('fast'); $('#grey-cover').remove();
    });
	
	
	/* Item gallery
	-----------------------------------------------------------------------------*/
	if ($('#gallery').height() > 0) {
		$('#gallery').slides({
			preload: false,
			preloadImage: 'img/loading.gif',
			effect: 'fade',
			crossfade: true,
			slideSpeed: 350,
			fadeSpeed: 500,
			generateNextPrev: false,
			generatePagination: false
		});
	}
	
	
	/* Input counting
	-----------------------------------------------------------------------------*/
	$('.counting').each(function() {
        var count = $(this);
        count.find('a:first-child').click(function() {
            var data = count.find('input').val();
            if(data > 1) {
                count.find('input').val(parseInt(data) - 1);
            }
        });
        count.find('a:last-child').click(function() {
            var data = count.find('input').val();
            count.find('input').val(parseInt(data) + 1);
        });
    });
	
	/* Rwmove from cart
	-----------------------------------------------------------------------------*/
	$("#cartItems .remove a").click(function() {
		$(this).parent().parent("tr").hide();
     });
	
});





















