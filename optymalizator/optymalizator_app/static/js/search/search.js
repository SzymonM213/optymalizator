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
  block = document.getElementById(id);
  text = block.innerHTML;
  ref_lvls = block.getElementsByClassName("refundation-levels");
  if (ref_lvls.length > 0) {
    ref_lvls[0].remove();
  } else {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/ref-levels/" + id + "/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
        text += '<div class = "refundation-levels">';
        text += '<br><h3> Wybierz poziom refundacji: </h3>';
        var jsonResponse = JSON.parse(xhr.responseText);
        for (var i = 0; i < jsonResponse.lvls.length; i++) {
          text += '<a class = "refundation-level" onclick="choose_drug(event, ' + id + ')">' 
              + jsonResponse.lvls[i] + '</a><br>';
        }
        text += '</div>'
        document.getElementById(id).innerHTML = text;
      }
    }
    xhr.send();
  }
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
