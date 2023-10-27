const current_url = window.location.href.toString().split(window.location.host)[1];
let graph_request;
let preset_request;
let history_request;

let cur_history_page = 1;

$(document).on("submit", function (event) {
    event.preventDefault();
});

function updateGraph(is_authorized, csrftoken) {
    let request_data = getFormFields();

    if (graph_request && graph_request.readyState !== 4) {
        graph_request.abort();
    }

    graph_request = $.ajax({
        url: current_url + "graph/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: request_data,
        beforeSend: function () {
            $("#graph").html(
                "<svg class=\"spinner\" viewBox=\"0 0 50 50\">" +
                "    <circle class=\"path\" cx=\"25\" cy=\"25\" r=\"20\" fill=\"none\" stroke-width=\"5\"></circle>" +
                "</svg>"
            );
        },
        success: function (response) {
            if (response === "None") {
                $("#graph").html(
                    "<div class=\"alert alert-warning text-center\" role=\"alert\">" +
                    "    <p>Не удалось сгенерировать график</p>" +
                    "</div>"
                );
            } else {
                $("#graph").html(response);
            }
        },
        error: function (jqXHR, exception) {
            $("#graph").html(processError(jqXHR, exception));
        }
    });

    if (is_authorized) {
        updateHistory(csrftoken);
    }
}

function getReport(is_authorized, csrftoken) {
    let request_data = getFormFields();

    if (graph_request && graph_request.readyState !== 4) {
        graph_request.abort();
    }

    graph_request = $.ajax({
        url: current_url + "graph-report/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: request_data,
        xhrFields: {
            responseType: 'blob'
        },
        success: function (data) {
            const blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "filename.docx";
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        },
        error: function (jqXHR, exception) {
            alert(processError(jqXHR, exception));
        }
    });
}


    function savePreset(csrftoken) {
        let request_data = getFormFields();
        request_data["preset_operation"] = "save_preset";

        if (preset_request && preset_request.readyState !== 4) {
            preset_request.abort();
        }

        preset_request = $.ajax({
            url: current_url + "preset/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: request_data,
            success: function (response) {
                $("#presets").html(response);

                let save_preset_element = document.getElementById("save_preset");
                if (!save_preset_element.disabled && response.split("<tr>").length - 2 >= 5) {
                    save_preset_element.disabled = true;
                }
            }
        });
    }

    function deletePreset(id, csrftoken) {
        if (preset_request && preset_request.readyState !== 4) {
            preset_request.abort();
        }

        preset_request = $.ajax({
            url: current_url + "preset/",
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

        if (history_request && history_request.readyState !== 4) {
            history_request.abort();
        }

        history_request = $.ajax({
            url: current_url + "history/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: Object.assign({}, request_data, {"page": cur_history_page}),
            success: function (response) {
                $("#history").html(response);
            }
        });
    }

    function getHistoryPage(csrftoken, page) {
        cur_history_page = page;

        if (history_request && history_request.readyState !== 4) {
            history_request.abort();
        }

        history_request = $.ajax({
            url: current_url + "history",
            data: {
                page: cur_history_page
            },
            type: "GET",
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (response) {
                $("#history").html(response);
            }
        });
    }

    function getFormFields() {
        let request_data = {};

        $("#interferometer input").each(function (_, value) {
            if (value.hasAttribute("type") && value.getAttribute("type") === "number") {
                request_data[value.id.slice(3)] = value.value;
            }
        });

        return request_data;
    }

    function processError(jqXHR, exception) {
        let message;

        if (exception === "abort") {
            message = "Запрос прерван";
        } else if (exception === "parsererror") {
            message = "Ошибка чтения ответа сервера";
        } else if (exception === "timeout") {
            message = "Превышено время ожидания";
        } else if (jqXHR.status === 0) {
            message = "Не удалось выполнить запрос";
        } else if (jqXHR.status === 404) {
            message = 'Запрашиваемая страница не найдена';
        } else if (jqXHR.status === 500) {
            message = "Ошибка сервера";
        } else {
            message = "Неизвестная ошибка";
        }

        return "<div class=\"alert alert-warning text-center\" role=\"alert\">" +
            "    <p>" + message + "</p>" +
            "</div>"
    }
