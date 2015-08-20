$(function() {
	
	
	/* Table corner classes
	-----------------------------------------------------------------------------*/
	if ($('table.styled').height() > 0) {
		$('.styled tr:first-child th:last').addClass('top-right-corner');
		$('.styled tr:last td:first-child').addClass('bottom-left-corner');
		$('.styled tr:last td:last').addClass('bottom-right-corner');
	}
	
    /* Search input clear
	-----------------------------------------------------------------------------*/
	var q = $('.search input[type=text], .autoclear');
	q.focus(function() {
	    if ($(this).attr('data-default') == $(this).val()) {
	        $(this).val('');
	    }
	}).blur(function() {
	    if($(this).val() == '') {
	        $(this).val($(this).attr('data-default'));
	    }
	});
	
    
    /* Brands carousel
	-----------------------------------------------------------------------------*/
    $('#brands').jcarousel({
        'wrap': 'none'
    });
    
    $('.prev-brand').jcarouselControl({
        target: '-=4'
    });
    $('.next-brand').jcarouselControl({
        target: '+=4'
    });
    
    
    /* Item detail gallery
	-----------------------------------------------------------------------------*/
    $('#thumbs').jcarousel({
        'wrap': 'none'
    });
    $('#photo a:first').css('display', 'block');
    
    
    $('.prev-photo').jcarouselControl({
        target: '-=3'
    });
    $('.next-photo').jcarouselControl({
        target: '+=3'
    });
    
    $('#thumbs a').click(function(e) {
    	var clicked = $(e.target),
		    imdData = $(this).attr('href').substring(1);
		    
		if (!$(this).hasClass('active')) {
			$('#photo a').fadeOut(); $('#thumbs a').removeClass('active');
			$(this).addClass('active');
			$('#photo').find("a[data-img='"+imdData+"']").fadeIn();
		}
		return false;
    });
    
    
    /* Autocomplete
	-----------------------------------------------------------------------------*/
	$.fn.cssUnit = function(key) {
	    var style = this.css(key), val = [];
	    $.each( ['em','px','%','pt'], function(i, unit){
	        if(style.indexOf(unit) > 0)
	            val = [parseFloat(style), unit];
	    });
	    return val;
	}
	
    var availableTags = [
			"ActionScript",
			"AppleScript",
			"Asp",
			"BASIC",
			"C",
			"C++",
			"Clojure",
			"COBOL",
			"ColdFusion",
			"Erlang",
			"Fortran",
			"Groovy",
			"Haskell",
			"Java",
			"JavaScript",
			"Lisp",
			"Perl",
			"PHP",
			"Python",
			"Ruby",
			"Scala",
			"Scheme"
		];
		$( "#autocomplete" ).autocomplete({
			source: availableTags,
	        'open': function(e, ui) {
	            $('.ui-autocomplete').css('top', $("ul.ui-autocomplete").cssUnit('top')[0] + 2);
	        }
		});
		
		
	/* Show popup
	-----------------------------------------------------------------------------*/
	$('.show-popup').click(function(e) {
		var clicked = $(e.target),
		    blockID = $(this).attr('href');
		    
		if ($(this).hasClass('active')) {
			$(this).removeClass('active');
			$(blockID).fadeOut("fast");
		} else {
			$('.show-popup').removeClass('active');
			$(this).addClass('active');
			$(".popup-block").fadeOut("fast");
			$(blockID).fadeIn('fast');
		}
		return false;
	});		
	
	/* Close popup
	-----------------------------------------------------------------------------*/
	$(document).click(function(e) {
		var clicked = $(e.target);
		if (!clicked.parents().hasClass("popup-block") && !clicked.hasClass("popup-block")) {
			$(".popup-block").fadeOut("fast");
			$('.show-popup').removeClass('active');
		}
	});	
	
	
	/* Tooltip
	-----------------------------------------------------------------------------*/
	$('a.tip').tooltip({
		position: {
			my: "left-125 top+20",
			at: "center top",
			using: function(position, feedback) {
				$(this).css(position);
				$("<div>")
				.addClass("arrow")
				.addClass(feedback.vertical)
				.addClass(feedback.horizontal)
				.appendTo(this);
			}
		}
	});
	 
	 
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
	
	
	/* Enter only digits in counting inputs
	-----------------------------------------------------------------------------*/
	$(".counting input, .price-range input, .user-profile-edit .date input").keydown(function(event) {
        // Allow: backspace, delete, tab, escape, and enter
        if ( event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 || 
             // Allow: Ctrl+A
            (event.keyCode == 65 && event.ctrlKey === true) || 
             // Allow: home, end, left, right
            (event.keyCode >= 35 && event.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        else {
            // Ensure that it is a number and stop the keypress
            if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                event.preventDefault(); 
            }   
        }
    }); 
    
	
	/* Tabs
	-----------------------------------------------------------------------------*/
	$('#tabs').tabs();
    
    
    /* Selects
	-----------------------------------------------------------------------------*/
	$('select').styler();
	
	
	/* Ordering submit
	-----------------------------------------------------------------------------*/
	$('#agree label').on("click", function() {
		if ($('#agree input[type=checkbox]').is(':checked')) $(this).parent().find('.button').removeClass('disable');
		else $(this).parent().find('.button').addClass('disable');
	});
	
	$('#agree input[type=button]').on("click", function() {
		if (!$(this).hasClass('disable')) $('#ordering').submit();
		else return false;
	});
	
	
	/* FAQ
	-----------------------------------------------------------------------------*/
	$(document).on('click', '#faq .show', function() {
		
		var autoHeight = $(this).parents('.more').find('.text').height();
		
		$(this).removeClass('show').addClass('hide').text('Свернуть');
		
		$(this).parents('.more').animate({
			height: autoHeight + 27
		}, 500, function() {

		});
		return false;
	});

	$(document).on('click', '#faq .hide', function() {
		
		$(this).removeClass('hide').addClass('show').text('Развернуть');
		
		$(this).parents('.more').animate({
			height: 95
		}, 500, function() {

		});
		return false;
	});
	
	
	/* Обрезка текста
	-----------------------------------------------------------------------------*/
	$('.catalog-items .items-list .intro').jTruncate({ 
		length: 90, 
		minTrail: 0, 
		moreText: "", 
		lessText: "", 
		ellipsisText: "...", 
		moreAni: "fast", 
		lessAni: 2000 
	});  
	
});