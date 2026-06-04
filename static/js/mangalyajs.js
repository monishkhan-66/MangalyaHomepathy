document.addEventListener("DOMContentLoaded", function () {
  // ---------------- Counter Animation ----------------
  const counters = document.querySelectorAll(".counter");
  counters.forEach(counter => {
    const target = +counter.getAttribute("data-target");
    const speed = 200;
    const increment = Math.ceil(target / speed);

    const updateCount = () => {
      const current = parseInt(counter.innerText.replace("+", ""), 10) || 0;
      if (current < target) {
        counter.innerText = current + increment + "+";
        setTimeout(updateCount, 20);
      } else {
        counter.innerText = target.toLocaleString() + "+";
      }
    };
    updateCount();
  });

  // ---------------- Navbar Toggler Icon Change ----------------
  const toggler = document.getElementById("navbarToggler");
  if (toggler) {
    toggler.addEventListener("click", function () {
      const icon = this.querySelector("i");
      if (icon.classList.contains("fa-bars")) {
        icon.classList.remove("fa-bars");
        icon.classList.add("fa-times");
      } else {
        icon.classList.remove("fa-times");
        icon.classList.add("fa-bars");
      }
    });
  }
});

// ---------------- Sidebar Functions ----------------
function openSidebar() {
  document.getElementById("mySidebar").classList.add("open");
  document.getElementById("overlay").classList.add("active");
  document.getElementById("toggleSidebarBtn").style.display = "none";
}

function closeSidebar() {
  document.getElementById("mySidebar").classList.remove("open");
  document.getElementById("overlay").classList.remove("active");
  document.getElementById("toggleSidebarBtn").style.display = "block";
}

// ---------------- Google Reviews Toggle (Optional) ----------------
// function toggleReviews() {
//   const section = document.getElementById("google-reviews-container");
//   const button = event.target;
//   section.classList.toggle("d-none");
//   button.innerText = section.classList.contains("d-none") ? "Show Google Reviews" : "Hide Google Reviews";
// }
