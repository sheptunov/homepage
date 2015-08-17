function include(scriptUrl) {
    document.write('<script src=/static/portfolio/js/' + scriptUrl + '></script>');
}

function isIE() {
    var myNav = navigator.userAgent.toLowerCase();
    return (myNav.indexOf('msie') != -1) ? parseInt(myNav.split('msie')[1]) : false;
}

/* cookie.JS
 ========================================================
 include('jquery.cookie.js');
 */

/* Easing library
 ========================================================*/
(function ($) {
    include('jquery.easing.1.3.js');
})(jQuery);

/* Stick up menus
 ========================================================*/
(function ($) {
    var o = $('html');
    if (o.hasClass('desktop')) {
        include('tmstickup.js');

        $(document).ready(function () {
            $('#topmenu').TMStickUp({})
        });
    }
})(jQuery);


/* ScrollTop
 ========================================================*/
(function ($) {
    var o = $('html');
    if (o.hasClass('desktop')) {
        include('jquery.ui.totop.js');

        $(document).ready(function () {
            $().UItoTop({
                easingType: 'easeOutQuart',
                containerClass: 'toTop fa fa-angle-up'
            });
        });
    }
})(jQuery);

/* EqualHeights
 ========================================================*/
(function ($) {
    var o = $('[data-equal-group]');
    if (o.length > 0) {
        include('jquery.equalheights.js');
    }
})(jQuery);

/* SMOOTH SCROLLIG
 ========================================================*/
(function ($) {
    var o = $('html');
    if (o.hasClass('desktop')) {
        include('jquery.mousewheel.min.js');
        include('jquery.simplr.smoothscroll.min.js');

        $(document).ready(function () {
            $.srSmoothscroll({
                step: 150,
                speed: 800
            });
        });
    }
})(jQuery);


/* Navbar
 ========================================================

 (function ($) {
 include('jquery.rd-navbar.js');
 })(jQuery);
 */

/* WOW
 ========================================================*/
(function ($) {
    var o = $('html');

    if ((navigator.userAgent.toLowerCase().indexOf('msie') == -1 ) || (isIE() && isIE() > 9)) {
        if (o.hasClass('desktop')) {
            include('wow.js');

            $(document).ready(function () {
                //function wowinit() {
                new WOW({
                    boxClass:     'wow',      // default
                    animateClass: 'animated', // default
                    offset:       0,          // default
                    mobile:       false,       // default
                    live:         false        // default
                }).init();
                //}
                //setTimeout(wowinit, 1000)
            })
        }
    }
})(jQuery);

/* Orientation tablet fix
 ========================================================*/
$(function () {
    // IPad/IPhone
    var viewportmeta = document.querySelector && document.querySelector('meta[name="viewport"]'),
        ua = navigator.userAgent,

        gestureStart = function () {
            viewportmeta.content = "width=device-width, minimum-scale=0.25, maximum-scale=1.6, initial-scale=1.0";
        },

        scaleFix = function () {
            if (viewportmeta && /iPhone|iPad/.test(ua) && !/Opera Mini/.test(ua)) {
                viewportmeta.content = "width=device-width, minimum-scale=1.0, maximum-scale=1.0";
                document.addEventListener("gesturestart", gestureStart, false);
            }
        };

    scaleFix();
    // Menu Android
    if (window.orientation != undefined) {
        var regM = /ipod|ipad|iphone/gi,
            result = ua.match(regM);
        if (!result) {
            $('.sf-menus li').each(function () {
                if ($(">ul", this)[0]) {
                    $(">a", this).toggle(
                        function () {
                            return false;
                        },
                        function () {
                            window.location.href = $(this).attr("href");
                        }
                    );
                }
            })
        }
    }
});
var ua = navigator.userAgent.toLocaleLowerCase(),
    regV = /ipod|ipad|iphone/gi,
    result = ua.match(regV),
    userScale = "";
if (!result) {
    userScale = ",user-scalable=0"
}
document.write('<meta name="viewport" content="width=device-width,initial-scale=1.0' + userScale + '">');

/* Responsive Tabs
 ========================================================*/

(function ($) {
    var o = $('.resp-tabs');
    if (o.length > 0) {
        include('jquery.responsive.tabs.js');

        $(document).ready(function () {
            o.easyResponsiveTabs();
        });
    }
})(jQuery);

/* FancyBox
 ========================================================*/




/* Topmenu scrollclass y
 ========================================================*/
(function ($) {
    menu = $(".block_topmenu_sticky");
    $('.block-about').scrollClass({
        delay: 0, //set class after 20 milliseconds delay
        threshold: 0, //set class when 50% of element enters the viewport
        offsetTop: 0, //height in pixels of a fixed top navbar
        callback: function () { //fire a callback
            $("li", menu).removeClass('active');
            $(".about", menu).toggleClass('active')
        }
    });
    $('.block-skills').scrollClass({
        delay: 0, //set class after 20 milliseconds delay
        threshold: 0, //set class when 50% of element enters the viewport
        offsetTop: 0, //height in pixels of a fixed top navbar
        callback: function () { //fire a callback
            $("li", menu).removeClass('active');
            $(".skills", menu).toggleClass('active')
        }
    });
    /*
    $('.block-benefits').scrollClass({
        delay: 0, //set class after 20 milliseconds delay
        threshold: 0, //set class when 50% of element enters the viewport
        offsetTop: 0, //height in pixels of a fixed top navbar
        callback: function () { //fire a callback
            $("li", menu).removeClass('active');
            $(".benefits", menu).toggleClass('active')
        }
    });
    */
    $('.block-projects').scrollClass({
        delay: 0, //set class after 20 milliseconds delay
        threshold: 0, //set class when 50% of element enters the viewport
        offsetTop: 0, //height in pixels of a fixed top navbar
        callback: function () { //fire a callback
            $("li", menu).removeClass('active');
            $(".projects", menu).toggleClass('active')
        }
    });
    $('.block-feedback').scrollClass({
        delay: 0, //set class after 20 milliseconds delay
        threshold: 0, //set class when 50% of element enters the viewport
        offsetTop: 0, //height in pixels of a fixed top navbar
        callback: function () { //fire a callback
            $("li", menu).removeClass('active');
            $(".feedback", menu).toggleClass('active')
        }
    });
})(jQuery);

