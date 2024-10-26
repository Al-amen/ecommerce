$('.intro-slider').on('initialized.owl.carousel', function() {
    $('.intro-slide').each(function() {
        const bg = $(this).data('bg');
        $(this).css('background-image', 'url(' + bg + ')');
    });
});



  // Lazy Load Images
  document.addEventListener("DOMContentLoaded", function() {
    const lazyImages = document.querySelectorAll('img.lazy');

    const lazyLoad = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.src = entry.target.dataset.src;
                observer.unobserve(entry.target);
            }
        });
    };

    const observer = new IntersectionObserver(lazyLoad, {
        rootMargin: "0px 0px 200px 0px"
    });

    lazyImages.forEach(image => {
        observer.observe(image);
    });
});

// Ensure images are loaded and banners appear correctly
document.addEventListener("DOMContentLoaded", function() {
    const banners = document.querySelectorAll('.banner img');
    banners.forEach(function(banner) {
        banner.addEventListener('load', function() {
            banner.style.opacity = '1';
        });
    });

    const maxBannerHeight = Math.max(...Array.from(banners).map(b => b.offsetHeight));
    banners.forEach(function(banner) {
        banner.style.height = maxBannerHeight + 'px';
    });
});