const current_url = window.location.href.toString().split(window.location.host)[1];

$(document).on("submit", function(event) {
    event.preventDefault();
});

function updateGraph(is_authorized, csrftoken) {
    let request_data = getFormFields();

    $.ajax({
        url: current_url + "update_graph/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: request_data,
        timeout: 10000,
        beforeSend: function() {
            $("#graph").html(
                "<svg class=\"spinner\" viewBox=\"0 0 50 50\">" +
                "    <circle class=\"path\" cx=\"25\" cy=\"25\" r=\"20\" fill=\"none\" stroke-width=\"5\"></circle>" +
                "</svg>"
            );
        },
        success: function(response) {
            if (response === "None") {
                $("#graph").html(
                    "<div class=\"alert alert-warning text-center\" role=\"alert\">" +
                    "    <p>Не удалось сгенерировать график.</p>" +
                    "</div>"
                );
            }
            else
                $("#graph").html(response);
        },
        error: function(jqXHR, exception) {
            let message = "";

            if (exception === "timeout") {
                message = "Превышено время ожидания.";
            } else if (exception === "abort") {
                message = "Запрос прерван.";
            } else if (jqXHR.status === 0) {
                message = "Не удалось выполнить запрос. Попробуйте позже.";
            } else if (jqXHR.status === 500) {
                message = "Ошибка сервера.";
            } else {
                message = "Неизвестная ошибка.";
            }

            $("#graph").html(
                "<div class=\"alert alert-warning text-center\" role=\"alert\">" +
                "    <p>" + message + "</p>" +
                "</div>"
            );
        }
    });

    if (is_authorized) {
        updateHistory(csrftoken);
    }
}

function savePreset(csrftoken) {
    let request_data = getFormFields();
    request_data["preset_operation"] = "save_preset";

    $.ajax({
        url: current_url + "update_preset/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: request_data,
        success: function (response) {
            $("#presets").html(response);

            let save_preset_element = document.getElementById("save_preset");
            if (! save_preset_element.disabled && response.split("<tr>").length - 2 >= 5) {
                save_preset_element.disabled = true;
            }
        }
    });
}

function deletePreset(id, csrftoken) {
    $.ajax({
        url: current_url + "update_preset/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: {
            "delete_preset": id,
            "preset_operation": "delete_preset"
        },
        success: function (response) {
            $("#presets").html(response);

            let save_preset_element = document.getElementById("save_preset");
            if (save_preset_element.disabled) {
                save_preset_element.disabled = false;
            }
        }
    });
}

function updateHistory(csrftoken) {
    let request_data = getFormFields();

    $.ajax({
        url: current_url + "update_history/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: request_data,
        success: function(response) {
            $("#history").html(response);
        }
    });
}

function getFormFields() {
    let request_data = {};

    $("#interferometer input").each(function(_, value) {
        if (value.hasAttribute("type") && value.getAttribute("type") === "number") {
            request_data[value.id.slice(3)] = value.value;
        }
    });

    return request_data;
}
