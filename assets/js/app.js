(function ($) {
  "use strict";
      
      
  
  /*--------------------------
  preloader
  ---------------------------- */	
  
  $(window).on('load',function(){
      var pre_loader = $('#preloader')
  pre_loader.fadeOut('slow',function(){$(this).remove();});
  });	
  
  // meanmenu
  $('#mobile-menu').meanmenu({
    meanMenuContainer: '.mobile-menu',
    meanScreenWidth: "992"
  });
      
  /*------------------------------------
   search option
  ------------------------------------- */ 
    
      $('.search-option').hide();
      $(".main-search").on('click', function(){
          $('.search-option').animate({
              height:'toggle',
          });
      });
  
  /*---------------------
   TOP Menu Stick
  --------------------- */
    
  var windows = $(window);
  var sticky = $('#sticker');
  
  windows.on('scroll', function() {
      var scroll = windows.scrollTop();
      if (scroll < 300) {
          sticky.removeClass('stick');
      }else{
          sticky.addClass('stick');
      }
  });
  // Tab-click-js
  var collapseElementList = [].slice.call(document.querySelectorAll('.collapse'))
  var collapseList = collapseElementList.map(function (collapseEl) {
    return new bootstrap.Collapse(collapseEl)
  })
      
  /* magnificPopup video view */
  $('.popup-video').magnificPopup({
    type: 'iframe'
  });
      
   
  
  /*---------------------
   wow .js
  --------------------- */
      function wowAnimation(){
          new WOW({
              offset: 100,          
              mobile: true
          }).init()
      }
      wowAnimation()	
      
  // scrollToTop
  $.scrollUp({
    scrollName: 'scrollUp', // Element ID
    topDistance: '300', // Distance from top before showing element (px)
    topSpeed: 300, // Speed back to top (ms)
    animation: 'fade', // Fade, slide, none
    animationInSpeed: 200, // Animation in speed (ms)
    animationOutSpeed: 200, // Animation out speed (ms)
    scrollText: '<i class="ti-arrow-up"></i>', // Text for element
    activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
  });
    
  
    // data - background
    $("[data-background]").each(function () {
      $(this).css("background-image", "url(" + $(this).attr("data-background") + ")")
    })
  
    $("[data-bg-color]").each(function () {
      $(this).css("background", $(this).attr("data-bg-color"))
    })
  
      
  /*---------------------
    venobox
  --------------------- */
    var veno_box = $('.venobox');
    veno_box.venobox();
  
  /*--------------------------
       Project carousel
  ---------------------------- */
    var project_carousel = $('.project-carousel');
    project_carousel.owlCarousel({
          loop:true,
          nav:true,		
          autoplay:false,
          margin: 30,
          dots:false,
          navText: ["<i class='ti-angle-left'></i>","<i class='ti-angle-right'></i>"],
          responsive:{
              0:{
                  items:1
              },
              700:{
                  items:2
              },
              1000:{
                  items:3
              }
          }
      });
  /*---------------------
   Testimonial carousel
  ---------------------*/
    
      var review = $('.testimonial-carousel');
      review.owlCarousel({
      loop:true,
      nav:true,
          margin:30,
      center:true,
          navText: ["<i class='ti-angle-left'></i>","<i class='ti-angle-right'></i>"],
      dots:false,
      autoplay:false,
      responsive:{
        0:{
          items:1
        },
        768:{
          items:1
        },
        1000:{
          items:2
        }
      }
    });
  /*---------------------
   Brand carousel
  ---------------------*/
    
      var brand = $('.brand-carousel');
      brand.owlCarousel({
      loop:true,
      nav:false,
          margin:30,
      dots:true,
      autoplay:false,
      responsive:{
        0:{
          items:1
        },
        768:{
          items:4
        },
        1000:{
          items:5
        }
      }
    });
  
      
      
  /*--------------------------
       Project Details carousel 
  ---------------------------- */
      $('.project-carousel-2').owlCarousel({
          loop:true,
          nav:true,		
          autoplay:true,
          dots:false,
      margin:30,
          navText: ["<i class='ti-angle-left'></i>","<i class='ti-angle-right'></i>"],
          responsive:{
              0:{
                  items:1
              },
              700:{
                  items:2
              },
              1000:{
                  items:2
              }
          }
      });
  
    
    $('.counter').counterUp({
      delay: 10,
      time: 1000
    });

    $('.single-page-head .left-menu li').on('click', function(e) {
      $('.single-page-head .left-menu li').removeClass('active');
      $(this).addClass('active');
    });

    
    $('.infinite-scroll').infiniteScroll({
      path: function path() {
        var pageNumber = this.loadCount + 2;
        return '/blog/pages/' + pageNumber + '/index.html';
      },
      append: '.post-item',
      button: '.loadmore',
      scrollThreshold: false

    });

    // search 
    var sjs = SimpleJekyllSearch({
      searchInput: document.getElementById('search-input'),
      resultsContainer: document.getElementById('results-container'),
      json: '/search.json',
      searchResultTemplate: '<div class="search-results"><a class="gh-search-item" href="{url}"><h5 class="search-post-title">{title}</h5></a>'
    });

    document.querySelector('.main-search').addEventListener('click', function(e){
      e.preventDefault();
    });

    jQuery('.service-tab .nav-link').on('click', function(e){
      e.preventDefault();
      $('.service-tab .nav-link').removeClass('active')
      $('.service-tab .nav-link').removeClass('show')
      
      $(this).addClass('active')
      $(this).addClass('show')

      let elementID = $(this).attr('href');

      $('.tab-pane').removeClass('active');
      $('.tab-pane').removeClass('show');

      $(elementID).addClass('active');
      $(elementID).addClass('show');
      
      
    });
  
  })(jQuery);
  