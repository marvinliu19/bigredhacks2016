$(function () {
    $('a[href*=#]:not([href=#])').click(function () {
        var target = $(this).attr('href');
        $('.parallax').animate({
            scrollTop: $(target).offset().top + $('.parallax').scrollTop()
        }, 2500);
        return false;
    });
});
$(document).ready(function () {
    $(".navbar-nav li a").click(function (event) {
        $(".navbar-collapse").collapse('hide');
    });
});