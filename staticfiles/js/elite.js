// === GLOBAL SCROLL CONTROL ===
let ticking = false;
let isAnimating = false;
let scrollAmount = 0;
let isHorizontal = true;

window.addEventListener("scroll", () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      handleScrollEvents();
      ticking = false;
    });
    ticking = true;
  }
});

function handleScrollEvents() {
  const scrollY = window.scrollY;
  const innerHeight = window.innerHeight;
  const docHeight = document.documentElement.scrollHeight - innerHeight;
  const scrollPercentage = (scrollY / docHeight) * 100;

  // 1. Navbar background
  const navbar = document.getElementById("container");
  if (navbar) navbar.style.backgroundColor = scrollY > 50 ? "#1b1b1b" : "transparent";

  // 2. Goto buttons visibility
  toggleElement("goto", scrollY > 100);
  toggleElement("goto2", scrollY > 200);
  toggleElement("goto3", scrollY > 300);

  // 3. Progress bar width
  setWidth("line3", scrollPercentage + "%");
  setWidth("bg-grow2", (scrollPercentage * 3) + "%");
  setHeight("bg-grow", scrollPercentage + "%");

  // 4. Counter animation
  activateCounters(scrollY);

  // 5. Animate elements
  animateVisibleItems(".animation", "show");

  // 6. Animate images
  animateVisibleItems(".image-load", "show-image");
}

// === UTIL FUNCTIONS ===
function toggleElement(id, show) {
  const el = document.getElementById(id);
  if (el) el.style.display = show ? "block" : "none";
}
function setWidth(id, value) {
  const el = document.getElementById(id);
  if (el) el.style.width = value;
}
function setHeight(id, value) {
  const el = document.getElementById(id);
  if (el) el.style.height = value;
}

// === COUNTER ANIMATION ===
let countersActivated = false;
function activateCounters(scrollY) {
  const container = document.querySelector(".counters");
  if (!container || countersActivated) return;
  if (scrollY >= container.offsetTop - container.offsetHeight - 200) {
    document.querySelectorAll(".counter span[data-count]").forEach(counter => {
      const target = parseInt(counter.dataset.count);
      if (target > 500) {
        counter.innerText = "1 Lacs+";
      } else {
        animateCounter(counter, target);
      }
    });
    countersActivated = true;
  }
}

function animateCounter(counter, target) {
  let count = 0;
  const step = 1;
  function update() {
    count += step;
    if (count < target) {
      counter.innerText = count;
      requestAnimationFrame(update);
    } else {
      counter.innerText = target;
    }
  }
  update();
}

// === ELEMENT/IMAGE VISIBILITY (Intersection Observer) ===
function animateVisibleItems(selector, className) {
  const items = document.querySelectorAll(selector);
  items.forEach(item => {
    if (!item.classList.contains(className) && isInViewport(item)) {
      item.classList.add(className);
    }
  });
}
function isInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top < window.innerHeight &&
    rect.bottom > 0 &&
    rect.left < window.innerWidth &&
    rect.right > 0
  );
}

// === SCROLL TO TOP ===
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// === HORIZONTAL SCROLL (GSAP + Mouse + Touch) ===
document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll(".scroller-section");
  const scroller = document.querySelector(".scroller");
  const maxScroll = (sections.length - 1) * window.innerWidth;

  let touchStartX = 0;

  // Wheel Scroll
  window.addEventListener("wheel", (event) => {
    if (!isHorizontal) return;

    event.preventDefault();
    if (event.deltaY > 0 && scrollAmount < maxScroll) {
      scrollHorizontal(scroller, window.innerWidth);
    } else if (event.deltaY < 0 && scrollAmount > 0) {
      scrollHorizontal(scroller, -window.innerWidth);
    }

    if (scrollAmount >= maxScroll) {
      isHorizontal = false;
      document.body.style.overflowY = "auto";
    }
  }, { passive: false });

  // Touch Scroll
  window.addEventListener("touchstart", e => touchStartX = e.touches[0].clientX);

  window.addEventListener("touchmove", e => {
    if (isHorizontal) e.preventDefault();
  }, { passive: false });

  window.addEventListener("touchend", e => {
    const deltaX = touchStartX - e.changedTouches[0].clientX;
    if (isHorizontal && Math.abs(deltaX) > 50) {
      if (deltaX > 0 && scrollAmount < maxScroll) {
        scrollHorizontal(scroller, window.innerWidth);
      } else if (deltaX < 0 && scrollAmount > 0) {
        scrollHorizontal(scroller, -window.innerWidth);
      }
    }

    if (scrollAmount >= maxScroll) {
      isHorizontal = false;
      document.body.style.overflowY = "auto";
    }

    if (!isHorizontal && window.scrollY === 0) {
      isHorizontal = true;
      scrollAmount = maxScroll;
      document.body.style.overflowY = "hidden";
      reverseHorizontalScroll(scroller);
    }
  });

  // Reverse animation
  function reverseHorizontalScroll(scroller) {
    const interval = setInterval(() => {
      if (scrollAmount > 0) {
        scrollAmount -= window.innerWidth;
        gsap.to(scroller, { x: -scrollAmount, duration: 0.8, ease: "power2.out" });
      } else {
        clearInterval(interval);
      }
    }, 1000);
  }
});

// GSAP Horizontal Scroll Trigger
function scrollHorizontal(scroller, offset) {
  if (isAnimating) return;
  isAnimating = true;
  scrollAmount += offset;
  gsap.to(scroller, {
    x: -scrollAmount,
    duration: 0.8,
    ease: "power2.out",
    onComplete: () => isAnimating = false
  });
}

// === DYNAMIC WEB APP MANIFEST ===
const manifestData = {
  name: "",
  short_name: "",
  icons: [
    { src: "/android-chrome-192x192.png", sizes: "192x192", type: "image/png" },
    { src: "/android-chrome-512x512.png", sizes: "512x512", type: "image/png" }
  ],
  theme_color: "#ffffff",
  background_color: "#ffffff",
  display: "standalone"
};

const manifestJSON = JSON.stringify(manifestData, null, 2);
const link = document.createElement("link");
link.rel = "manifest";
const blob = new Blob([manifestJSON], { type: "application/json" });
link.href = URL.createObjectURL(blob);
document.head.appendChild(link);
