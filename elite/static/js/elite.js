
window.addEventListener("scroll", function() {
    let navbar = document.getElementById("container");
    if (window.scrollY > 50) { // Change color after 50px scroll
        navbar.style.backgroundColor="#1b1b1b";
        navbar.style.width="100vw"
    } else {
        navbar.style.backgroundColor="transparent";
    }
});
window.addEventListener("scroll", function() {
    let navbar = document.getElementById("goto");
    if (window.scrollY > 100) { // Change color after 50px scroll
        navbar.style.display="block";
    } else {
        navbar.style.display="none";
    }
});

window.addEventListener("scroll", () => {
  const navbar = document.getElementById("goto2");
  if (navbar) {
    navbar.style.display = window.scrollY > 200 ? "block" : "none";
  }
});

window.addEventListener("scroll", () => {
  const navbar = document.getElementById("goto3");
  if (navbar) {
    navbar.style.display = window.scrollY > 300 ? "block" : "none";
  }
});

window.addEventListener("scroll", function() {
    let scrollTop = window.scrollY;
    let docHeight = document.documentElement.scrollHeight - window.innerHeight;
    let scrollPercentage = (scrollTop / docHeight) * 100; // Calculate percentage

    let progressLine = document.getElementById("line3");
    progressLine.style.width = scrollPercentage + "%"; // Set width dynamically
});


window.addEventListener("scroll", function() {
    let scrollTop = window.scrollY;
    let docHeight = document.documentElement.scrollHeight - window.innerHeight;
    let scrollPercentage = (scrollTop / docHeight) * 100; // Just *100
    let progressLine = document.getElementById("bg-grow");
    progressLine.style.height = scrollPercentage + "%"; // Set height in %
});


window.addEventListener("scroll", function() {
    let scrollTop = window.scrollY;
    let docHeight = document.documentElement.scrollHeight - window.innerHeight;
    let scrollPercentage = (scrollTop / docHeight) * 300;

    let progressLine = document.getElementById("bg-grow2");
    progressLine.style.width = scrollPercentage + "%";
});


function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

const counters = document.querySelectorAll(".counter span[data-count]");
const container = document.querySelector(".counters");
let activated = false;

window.addEventListener("scroll", () => {
  if (
    window.pageYOffset >= container.offsetTop - container.offsetHeight - 200 &&
    !activated
  ) {
    counters.forEach(counter => {
      const target = parseInt(counter.dataset.count);
      let count = 0;

      if (target > 500) {
        counter.innerText = "1 Lacs+";
      } else {
        const increment = 1;
        function updateCount() {
          if (count < target) {
            count += increment;
            counter.innerText = count;
            setTimeout(updateCount, 15);
          } else {
            counter.innerText = formatCount(target);
          }
        }
        updateCount();
      }
    });
    activated = true;
  }
});

function formatCount(num) {
  if (num > 500) {
    return "1 Lacs+";
  }
  return num;
}



function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top < window.innerHeight && rect.bottom > 0 &&
        rect.left < window.innerWidth && rect.right > 0
    );
}

function animateOnScroll() {
    const elements = document.querySelectorAll('.animation');
    elements.forEach(element => {
        if (isInViewport(element) && !element.classList.contains('show')) {
            element.classList.add('show');
            element.getBoundingClientRect(); // Force repaint
        }
    });
}

function optimizedScroll() {
    requestAnimationFrame(animateOnScroll);
}

document.addEventListener('DOMContentLoaded', animateOnScroll);
window.addEventListener('scroll', optimizedScroll);


// animation2

function isInViewportImage(element) {
    const rect = element.getBoundingClientRect();
    return rect.top >= 0 && rect.left >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && rect.right <= (window.innerWidth || document.documentElement.clientWidth);
  }
  
  
  function imageOnScroll() {
    const images = document.querySelectorAll('.image-load');
    images.forEach(image => {
      if (isInViewport(image)) {
        image.classList.add('show-image');
      }
    });
  }
  
  window.addEventListener('scroll', imageOnScroll);
  window.addEventListener('load', imageOnScroll);
  
  imageOnScroll();


const manifestData = {
    name: "",
    short_name: "",
    icons: [
      {
        src: "/android-chrome-192x192.png",
        sizes: "192x192",
        type: "image/png"
      },
      {
        src: "/android-chrome-512x512.png",
        sizes: "512x512",
        type: "image/png"
      }
    ],
    theme_color: "#ffffff",
    background_color: "#ffffff",
    display: "standalone"
  };
  
  // Convert to JSON string if needed
  const manifestJSON = JSON.stringify(manifestData, null, 2);
  console.log(manifestJSON);
  
  // Optionally, dynamically add the manifest to your page
  const link = document.createElement('link');
  link.rel = 'manifest';
  
  // Create a Blob and URL for the manifest data
  const blob = new Blob([manifestJSON], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  link.href = url;
  document.head.appendChild(link);
  
  console.log('Manifest added dynamically!');
  


  

document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll(".scroller-section");
    const scroller = document.querySelector(".scroller");
    let scrollAmount = 0;
    let maxScroll = (sections.length - 1) * window.innerWidth; // Max horizontal scroll width
    let isHorizontal = true; // Tracks if scrolling is horizontal

    let touchStartX = 0, touchEndX = 0;

    // Handle Mouse Scroll
    window.addEventListener("wheel", function (event) {
        if (isHorizontal) {
            if (scrollAmount < maxScroll && event.deltaY > 0) {
                event.preventDefault();
                scrollAmount += window.innerWidth;
                gsap.to(scroller, { x: -scrollAmount, duration: 0.8, ease: "power2.out" });
            } else if (scrollAmount > 0 && event.deltaY < 0) {
                event.preventDefault();
                scrollAmount -= window.innerWidth;
                gsap.to(scroller, { x: -scrollAmount, duration: 0.8, ease: "power2.out" });
            }

            // Enable vertical scrolling when max horizontal scroll is reached
            if (scrollAmount >= maxScroll) {
                isHorizontal = false;
                document.body.style.overflowY = "auto"; // Enables vertical scrolling
            }
        } else {
            // Reverse scrolling order when scrolling back up
            if (window.scrollY === 0) {
                isHorizontal = true;
                scrollAmount = maxScroll; // Start from the last section
                reverseHorizontalScroll();
                document.body.style.overflowY = "hidden"; // Disable vertical scrolling
            }
        }
    });

    // Reverse Horizontal Scroll Animation
    function reverseHorizontalScroll() {
        let interval = setInterval(() => {
            if (scrollAmount > 0) {
                scrollAmount -= window.innerWidth;
                gsap.to(scroller, { x: -scrollAmount, duration: 0.8, ease: "power2.out" });
            } else {
                clearInterval(interval);
            }
        }, 1000); // Reverse scroll delay
    }

    // Handle Touch Start (Mobile)
    window.addEventListener("touchstart", function (event) {
        touchStartX = event.touches[0].clientX;
    });

    // Prevent Default Touch Scroll when in Horizontal Mode
    window.addEventListener("touchmove", function (event) {
        if (isHorizontal) {
            event.preventDefault();
        }
    }, { passive: false });

    // Handle Touch End (Swipe Detection)
    window.addEventListener("touchend", function (event) {
        touchEndX = event.changedTouches[0].clientX;
        let swipeDistance = touchStartX - touchEndX;

        if (isHorizontal) {
            if (swipeDistance > 50 && scrollAmount < maxScroll) {
                // Swipe Left (Next Section)
                scrollAmount += window.innerWidth;
                gsap.to(scroller, { x: -scrollAmount, duration: 0.8, ease: "power2.out" });
            } else if (swipeDistance < -50 && scrollAmount > 0) {
                // Swipe Right (Previous Section)
                scrollAmount -= window.innerWidth;
                gsap.to(scroller, { x: -scrollAmount, duration: 0.8, ease: "power2.out" });
            }

            if (scrollAmount >= maxScroll) {
                isHorizontal = false;
                document.body.style.overflowY = "auto"; // Enables vertical scrolling
            }
        } else {
            // Reverse horizontal scroll when scrolling back to top
            if (window.scrollY === 0) {
                isHorizontal = true;
                scrollAmount = maxScroll;
                reverseHorizontalScroll();
                document.body.style.overflowY = "hidden"; // Disable vertical scrolling
            }
        }
    });
});
