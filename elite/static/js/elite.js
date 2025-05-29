document.addEventListener("DOMContentLoaded", () => {
  const goto = document.getElementById("goto");
  const goto2 = document.getElementById("goto2");
  const goto3 = document.getElementById("goto3");
  const navbar = document.getElementById("container");
  const line3 = document.getElementById("line3");
  const bgGrow = document.getElementById("bg-grow");
  const bgGrow2 = document.getElementById("bg-grow2");
  const counters = document.querySelectorAll(".counter span[data-count]");
  const counterContainer = document.querySelector(".counters");

  let scrollTicking = false;
  let countersActivated = false;

  function handleScroll() {
    const scrollY = window.scrollY;
    const scrollBottom = window.innerHeight + scrollY;
    const docHeight = document.documentElement.scrollHeight;

    // Navbar background toggle
    if (navbar) {
      navbar.style.backgroundColor = scrollY > 50 ? "#222831" : "transparent";
      navbar.style.width = "100vw";
    }

    // Show/hide elements
    if (goto) goto.style.display = scrollY > 100 ? "block" : "none";
    if (goto2) goto2.style.display = scrollY > 200 && scrollBottom < docHeight - 50 ? "block" : "none";
    if (goto3) goto3.style.display = scrollY > 200 && scrollBottom < docHeight - 50 ? "block" : "none";

    // Progress lines
    const scrollProgress = (scrollY / (docHeight - window.innerHeight)) * 100;
    if (line3) line3.style.width = `${scrollProgress}%`;
    if (bgGrow) bgGrow.style.height = `${scrollProgress}%`;
    if (bgGrow2) bgGrow2.style.width = `${scrollProgress * 3}%`;

    // Counter activation
    if (
      counterContainer &&
      scrollY >= counterContainer.offsetTop - counterContainer.offsetHeight - 200 &&
      !countersActivated
    ) {
      countersActivated = true;
      counters.forEach(counter => {
        const target = parseInt(counter.dataset.count);
        let count = 0;

        if (target > 500) {
          counter.innerText = "1 Lacs+";
        } else {
          const increment = 1;
          const updateCount = () => {
            if (count < target) {
              count += increment;
              counter.innerText = count;
              setTimeout(updateCount, 15);
            } else {
              counter.innerText = target;
            }
          };
          updateCount();
        }
      });
    }

    // Animate .animation elements
    document.querySelectorAll(".animation").forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        el.classList.add("show");
      }
    });

    // Animate images
    document.querySelectorAll(".image-load").forEach(image => {
      const rect = image.getBoundingClientRect();
      if (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
      ) {
        image.classList.add("show-image");
      }
    });

    scrollTicking = false;
  }

  window.addEventListener("scroll", () => {
    if (!scrollTicking) {
      requestAnimationFrame(handleScroll);
      scrollTicking = true;
    }
  }, { passive: true });

  window.addEventListener("load", handleScroll); // Trigger scroll handler on page load
});

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
document.addEventListener("DOMContentLoaded", function () {
  const items = document.querySelectorAll(".professional-list li");
  let current = 0;

  function rotateActive() {
  items.forEach(item => item.classList.remove("active"));
  items[current].classList.add("active");
  current = (current + 1) % items.length;
}

setInterval(rotateActive, 2000); // Rotate every 3 seconds




// document.addEventListener('contextmenu', event => event.preventDefault());


// document.addEventListener('keydown', function(e) {
//     if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J')) || (e.ctrlKey && e.key === 'U')) {
//         e.preventDefault();
//     }
// });
