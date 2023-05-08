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
      'input': search.value,
    };

    console.log(data);
    return;

    // TODO: make it complient with docs, add error handling
    $.ajax({
      type: 'POST',
      url: '/search',
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
