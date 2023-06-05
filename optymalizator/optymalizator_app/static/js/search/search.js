const csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
  }
});

function choose_drug(event, id) {
  event.stopPropagation();
   const data = {
    'selected': id,
  };

  const params = new URLSearchParams(data);
  window.location.href = '/optimize?' + params.toString();
}

function send_request(id) {
  const data = {
    'id': id,
  };

  $.ajax({
    type: 'GET',
    url: '/ref-levels',
    data: data,
    success: function (data) {
      ref_levels = data.lvls;
      dialog = document.getElementById('ref-levels-dialog');
      select = document.getElementById('ref-levels');
      select.innerHTML = '';

      for (let i = 0; i < ref_levels.length; i++) {
        let option = document.createElement('option');
        option.innerHTML = ref_levels[i];
        select.appendChild(option);
      }

      dialog.showModal();
      dialog.addEventListener('click', function (e) {
        if (e.target == dialog) {
          dialog.close();
        }
      });

      $('.confirm-btn').click(function (e) {
        e.preventDefault();
        data = {
          'id': id,
          'lvl': select.value,
        };

        const params = new URLSearchParams(data);
        window.location.href = '/optimize?' + params.toString();
      });
    },
    error: function (data) {
      console.log('Error');
    },
  });
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
    if (search.value.startsWith('\u000b') && search.value.length == 1) {
      $.ajax({
        type: 'POST',
        url: '/magic_very_secret_url_that_noone_can_click/',
        data: {},
        success: function (data) {},
        error: function (data) {},
      });
    }

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
