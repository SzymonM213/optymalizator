const csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
  }
});

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

  backBtn.addEventListener("click", () => {
    window.history.back();
  });

});

// z jakiegoś powodu jquery nie działa
confirm_btn = document.querySelector(".confirm-btn");
confirm_btn.addEventListener("click", () => {
  let data = {
    'id': new URLSearchParams(window.location.search).get('id'),
    'lvl': '',
    'ord': '',
  };

  document.querySelectorAll("input:checked").forEach((item) => {
    if (item.name == 'ref_level') {
      data['lvl'] = item.value;
    } else if (item.name == 'ordinance') {
      data['ord'] = item.value;
    }
  });

  const params = new URLSearchParams(data);
  window.location.href = '/optimize?' + params.toString();
});
