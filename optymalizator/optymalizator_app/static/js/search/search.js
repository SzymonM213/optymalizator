const csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
  }
});

function send_request(id) {
  const data = {
    'selected': id,
  };

  const params = new URLSearchParams(data);
  window.location.href = '/optimize?' + params.toString();
}

$(document).ready(function() {
  topBtn = document.querySelector(".top-btn");
  backBtn = document.querySelector(".back-btn");

  // show button only when user scrolls down
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 100) {
      topBtn.classList.add("active");

      topBtn.addEventListener("click", () => {
        window.scrollTo(0, 0);
      });
    } else {
      topBtn.classList.remove("active");

      topBtn.removeEventListener("click", () => {
        window.scrollTo(0, 0);
      });
    }
  });

  searchBoxRight = document.querySelector('.search-box-right');
  search = document.getElementById("search");
  function submitSearch() {
    if (!search.value.trim()) return;

    const data = {
      'q': search.value
    };

    const params = new URLSearchParams(data);
    window.location.href = '/search?' + params.toString();
  }

  $('.search-form').submit(function(e) {
    e.preventDefault();
    submitSearch();
  });

  if (search.value == "") {
    searchBoxRight.classList.remove('active');
  } else {
    searchBoxRight.classList.add('active');
  }

  search.addEventListener('input', function () {
    if (search.value == "") {
      searchBoxRight.classList.remove('active');
    } else {
      searchBoxRight.classList.add('active');
    }
  })

  searchBoxRight.addEventListener('click', function () {
    if (searchBoxRight.classList.contains('active'))
      submitSearch();
  })
});
