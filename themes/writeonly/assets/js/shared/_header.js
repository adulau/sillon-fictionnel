document.addEventListener("DOMContentLoaded", () => {
  if ( window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ) {
    document.body.classList.add("dark");
  } else if ( window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ) {
    document.body.classList.remove("dark");
  }

  if ( localStorage.getItem("isDarkMode") === "true" ) {
    document.body.classList.add("dark");
    localStorage.setItem('isDarkMode', true);
  } else if ( localStorage.getItem("isDarkMode") === "false" ) {
    document.body.classList.remove("dark");
    localStorage.setItem('isDarkMode', false);
  }

  const lightDarkToggler = document.getElementById("light-dark-toggler");

  lightDarkToggler.addEventListener("click", (e) => {
    e.preventDefault();
    lightDarkToggle();
  });
});

function lightDarkToggle() {

  console.log(localStorage.getItem("isDarkMode"));

  if ( localStorage.getItem("isDarkMode") === "true" ) {
    document.body.classList.remove("dark");
    localStorage.setItem('isDarkMode', false);
  } else if ( localStorage.getItem("isDarkMode") === "false" ) {
    document.body.classList.add("dark");
    localStorage.setItem('isDarkMode', true);
  } else {
    document.body.classList.remove("dark");
    localStorage.setItem('isDarkMode', false);
  }
}

