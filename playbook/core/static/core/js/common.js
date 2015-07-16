function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function redirectToLogin(next) {
    url = "/accounts/login";
    if (next != null)
        url = url + "/?next=" + next;
    window.location.replace(url);
}

function showMessage(message) {
    var div = document.querySelector("#messages");
    div.textContent = message;
    $("#messages").show();
    setTimeout(function() { 
        div.textContent = ''; 
    }, 5000);
}

function showErrors(errors) {
    var string = "";
    er = JSON.parse(errors);
    for (field in er) { 
        for (error in er[field]) { 
            fieldObj = er[field];
            for (el in fieldObj) {
                if (field != "__all__")
                    string += field + ": "
                string += fieldObj[el].message + "\n";
            }
        }
    }
    showMessage(string);
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});