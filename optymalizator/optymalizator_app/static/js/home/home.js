const csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
  }
});

$(document).ready(function () {
  searchBoxRight = document.querySelector('.search-box-right');
  search = document.getElementById('search');

  search.addEventListener('input', function () {
    if (search.value == "") {
      searchBoxRight.classList.remove('active');
    } else {
      searchBoxRight.classList.add('active');
    }
  })

  function submitSearch() {
    if (!search.value.trim()) return;

    const data = {
      'q': search.value,
    };
    
    const params = new URLSearchParams(data);
    window.location.href = '/search?' + params.toString();
  }

  searchBoxRight.addEventListener('click', function () {
    if (searchBoxRight.classList.contains('active'))
      submitSearch();
  })

  $('.search-form').submit(function (e) {
    e.preventDefault();
    submitSearch();
  });
});
