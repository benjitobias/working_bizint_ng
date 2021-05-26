
window.addEventListener('load', function () {
  set_view_only(getCookie('view_only'));
})

function set_view_mode() {
    view_only = $("#view_only_switch").is(":checked");
    set_view_only(view_only);
}

function set_view_only(view_only) {
    if (view_only) {
        $('#view_only_switch').prop('checked', true);
        $('#add_button').prop('disabled', true);
        $('#id_update_telegram').prop('disabled', true);
        $('#id_note').prop('disabled', true);
        $('#id_ignore_location').prop('disabled', true);
        setCookie('view_only', 'true', 1)
    } else {
        $('#view_only_switch').prop('checked', false);
        $('#add_button').prop('disabled', false);
        $('#id_update_telegram').prop('disabled', false);
        $('#id_note').prop('disabled', false);
        $('#id_ignore_location').prop('disabled', false);
        setCookie('view_only', '', 1)
    }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}