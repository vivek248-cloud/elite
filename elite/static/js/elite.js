
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
    let scrollPercentage = (scrollTop / docHeight) * 100;

    let progressLine = document.getElementById("bg-grow");
    progressLine.style.height = scrollPercentage + "%";
});

window.addEventListener("scroll", function() {
    let scrollTop = window.scrollY;
    let docHeight = document.documentElement.scrollHeight - window.innerHeight;
    let scrollPercentage = (scrollTop / docHeight) * 70;

    let progressLine = document.getElementById("bg-grow2");
    progressLine.style.width = scrollPercentage + "%";
});


function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

//  counters
const counters = document.querySelectorAll(".counters span");
const container = document.querySelector(".counters");
let activated = false;
window.addEventListener("scroll",() => {
    if(
        pageYOffset >= container.offsetTop - container.offsetHeight - 200
        && activated === false
    )
    {
        counters.forEach(counter => {
            counter.innerText = 0;
            let count=0;

            function updateCount(){
                const target = parseInt(counter.dataset.count);
                if(count < target){
                   count++;
                   counter.innerText= count;
                   setTimeout(updateCount, 20);  
                }
                else{
                    counter.innerText = target;
                }
            }
            updateCount();
            activated = true;

        });

    } else if(
        pageYOffset < container.offsetTop - container.offsetHeight-500 
        || pageYOffset === 0
        && activated === true
    ){
        counters.forEach(counter => {
            counter.innerText = 0;
        });
        activated=false;
    }
});

// animation

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

//   mouse track

document.addEventListener("mousemove", function(event) {
    let cursor = document.querySelector(".cursor");

    // Update position with smooth animation
    cursor.style.transform = `translate(${event.clientX}px, ${event.clientY}px)`;
});


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
  


  
