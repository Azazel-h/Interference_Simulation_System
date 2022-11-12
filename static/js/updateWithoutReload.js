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
        success: function(response) {
            $("#graph").html(response);
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
