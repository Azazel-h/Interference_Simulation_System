$(document).on('submit', '#task-form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "index" %}',
        data: {
            task: $("#task").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
    })
});