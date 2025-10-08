(function ($) {
    'use strict';
    $('.mean-menu').meanmenu({meanScreenWidth: "1199"});
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 120) {
            $('.navbar-area').addClass("is-sticky");
        } else {
            $('.navbar-area').removeClass("is-sticky");
        }
    });
    $(function () {
        $('[data-bs-toggle="tooltip"]').tooltip()
    });
    $(".side-nav-responsive .dot-menu").on("click", function () {
        $(".side-nav-responsive .container-max .container").toggleClass("active");
    });
    $(function () {
        $('#sidemenu-nav').metisMenu();
    });
    $('.chat-list-header .header-right .favorite').on('click', function () {
        $(this).toggleClass('active');
    });
    $('.burger-menu').on('click', function () {
        $(this).toggleClass('active');
        $('.main-content').toggleClass('hide-sidemenu-area');
        $('.sidemenu-area').toggleClass('toggle-sidemenu-area');
        $('.top-navbar').toggleClass('toggle-navbar-area');
    });
    $('.responsive-burger-menu').on('click', function () {
        $('.responsive-burger-menu').toggleClass('active');
        $('.sidemenu-area').toggleClass('active-sidemenu-area');
    });
    $('.accordion').find('.accordion-title').on('click', function () {
        $(this).toggleClass('active');
        $(this).next().slideToggle('fast');
        $('.accordion-content').not($(this).next()).slideUp('fast');
        $('.accordion-title').not($(this)).removeClass('active');
    });
    $('.recent-job-slider').owlCarousel({
        loop: true,
        margin: 30,
        autoHeight: true,
        nav: false,
        dots: true,
        autoplay: true,
        autoplayHoverPause: true,
        responsive: {0: {items: 1,}, 768: {items: 2,}, 1000: {items: 2,}, 1200: {items: 3,},}
    })
    $('.company-slider').owlCarousel({
        loop: true,
        margin: 30,
        autoHeight: true,
        nav: false,
        dots: true,
        autoplay: true,
        autoplayHoverPause: true,
        responsive: {0: {items: 1,}, 768: {items: 2,}, 1000: {items: 3,}, 1200: {items: 4,},}
    })
    $('.testimonials-slider').owlCarousel({
        loop: true,
        margin: 30,
        autoHeight: true,
        nav: false,
        items: 1,
        dots: true,
        autoplay: true,
        autoplayHoverPause: true,
    })
    $('.testimonials-widget-slider').owlCarousel({
        loop: true,
        margin: 30,
        autoHeight: true,
        nav: false,
        items: 1,
        dots: true,
        autoplay: true,
        autoplayHoverPause: true,
    })
    $('.odometer').appear(function (e) {
        var odo = $(".odometer");
        odo.each(function () {
            var countNumber = $(this).attr("data-count");
            $(this).html(countNumber);
        });
    });
    $('.play-btn').magnificPopup({
        disableOn: 0,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });
    $('.gallery-photo').magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {enabled: true, navigateByImgClick: true, preload: [0, 1]}
    });
    $('.accordion-widget').find('.accordion-widget-title').on('click', function () {
        $(this).toggleClass('active');
        $(this).next().slideToggle('fast');
        $('.accordion-widget-content').not($(this).next()).slideUp('fast');
        $('.accordion-widget-title').not($(this)).removeClass('active');
    });
    if ($('.range-slider-area').length) {
        $(".range-slider-area .range-slider").slider({
            range: true,
            min: 1900,
            max: 2030,
            values: [1923, 2024],
            slide: function (event, ui) {
                $(".range-slider-area .count").text(ui.values[0] + " - " + ui.values[1]);
            }
        });
        $(".range-slider-area .count").text($(".range-slider").slider("values", 0) + " - " + $(".range-slider").slider("values", 1));
    }
    if ($('.area-range-slider').length) {
        $(".area-range-slider").slider({
            range: true, min: 0, max: 100, values: [0, 50], slide: function (event, ui) {
                $(".area-amount").text(ui.values[1]);
            }
        });
        $(".area-amount").text($(".area-range-slider").slider("values", 1));
    }

    function makeTimer() {
        var endTime = new Date("October 30, 2025 17:00:00 PDT");
        var endTime = (Date.parse(endTime)) / 1000;
        var now = new Date();
        var now = (Date.parse(now) / 1000);
        var timeLeft = endTime - now;
        var days = Math.floor(timeLeft / 86400);
        var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
        var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
        var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
        if (hours < "10") {
            hours = "0" + hours;
        }
        if (minutes < "10") {
            minutes = "0" + minutes;
        }
        if (seconds < "10") {
            seconds = "0" + seconds;
        }
        $("#days").html(days + "<span>Days</span>");
        $("#hours").html(hours + "<span>Hours</span>");
        $("#minutes").html(minutes + "<span>Minutes</span>");
        $("#seconds").html(seconds + "<span>Seconds</span>");
    }

    setInterval(function () {
        makeTimer();
    }, 300);
    $(".newsletter-form").validator().on("submit", function (event) {
        if (event.isDefaultPrevented()) {
            formErrorSub();
            submitMSGSub(false, "Please enter your email correctly");
        } else {
            event.preventDefault();
        }
    });

    function callbackFunction(resp) {
        if (resp.result === "success") {
            formSuccessSub();
        } else {
            formErrorSub();
        }
    }

    function formSuccessSub() {
        $(".newsletter-form")[0].reset();
        submitMSGSub(true, "Thank you for subscribing!");
        setTimeout(function () {
            $("#validator-newsletter").addClass('hide');
        }, 4000)
    }

    function formErrorSub() {
        $(".newsletter-form").addClass("animated shake");
        setTimeout(function () {
            $(".newsletter-form").removeClass("animated shake");
        }, 1000)
    }

    function submitMSGSub(valid, msg) {
        if (valid) {
            var msgClasses = "validation-success";
        } else {
            var msgClasses = "validation-danger";
        }
        $("#validator-newsletter").removeClass().addClass(msgClasses).text(msg);
    }

    $(".newsletter-form").ajaxChimp({
        url: "https://hibootstrap.us20.list-manage.com/subscribe/post?u=60e1ffe2e8a68ce1204cd39a5&amp;id=42d6d188d9",
        callback: callbackFunction
    });
    $('body').append("<div class='go-top'><i class='ri-arrow-up-s-line'></i></div>");
    $(window).on('scroll', function () {
        var scrolled = $(window).scrollTop();
        if (scrolled > 600) $('.go-top').addClass('active');
        if (scrolled < 600) $('.go-top').removeClass('active');
    });
    $('.go-top').on('click', function () {
        $('html, body').animate({scrollTop: '0',}, 500);
    });
    $(window).on('load', function () {
        $(".preloader").fadeOut(500);
    });
    $('body').append("<div class='switch-box'><label id='switch' class='switch'><input type='checkbox' onchange='toggleTheme()' id='slider'><span class='slider round'></span></label></div>");
})($);

function setTheme(themeName) {
    localStorage.setItem('zoben_theme', themeName);
    document.documentElement.className = themeName;
}

function toggleTheme() {
    if (localStorage.getItem('zoben_theme') === 'theme-dark') {
        setTheme('theme-light');
    } else {
        setTheme('theme-dark');
    }
}

(function () {
    if (localStorage.getItem('zoben_theme') === 'theme-dark') {
        setTheme('theme-dark');
        document.getElementById('slider').checked = false;
    } else {
        setTheme('theme-light');
        document.getElementById('slider').checked = true;
    }
})();