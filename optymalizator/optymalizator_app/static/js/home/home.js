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
    if (search.value == "") return;

    const data = {
      'input_text': search.value,
    };

    $.ajax({
      type: 'POST',
      url: 'search/',
      data: data,
      success: function (data) { location.reload(); },
    });
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
