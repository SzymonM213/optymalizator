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

  search = document.getElementById("search");
  function submitSearch() {
    if (search.value == "") return;

    const data = {
      'input_text': search.value
    };

    $.ajax({
      type: 'POST',
      url: '/get_search_results/',
      data: data,
      success: function(response) {
        if (response.json_list == null) return;
        html = ""
        for (i of response.json_list) {
          html += '<li class="card" id="' + i.id + '" onclick="send_request(' + i.id + ')">';
          html += '<p class="ean">EAN: ' + i.ean + '</p>';
          html += '<div class="main-content">';
          html += '<div class="left">';
          html += '<p>' + i.nazwa + '</p>';
          html += '<p>' + i.postac + '</p>';
          html += '<p>' + i.zawartosc_opakowania + '</p>';
          html += '<p>' + i.substancja_czynna + '</p>';
          html += '<p>' + i.dawka + '</p>';
          html += '</div>';
          html += '</div>';
          html += '</li>';
        }
        $('.drug-list').html(html);
      },
    });
  }

  $('.search-form').submit(function(e) {
    e.preventDefault();
    submitSearch();
  });
});
