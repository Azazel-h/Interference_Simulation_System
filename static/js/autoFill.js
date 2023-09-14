function fillValues(obj_names, row_id, form_fields, table) {
    let i = 0;

    while (i < obj_names.length) {
        if (obj_names[i] === "id" || obj_names[i] === "user" || obj_names[i] === "request_time") {
            obj_names.splice(i, 1);
            i--;
        }

        i++;
    }

    const source_tr = document.getElementById(table).children[1].children[row_id - 1];

    for (let i = 0; i < form_fields.length; i++) {
        let form_elem_id = "id_" + form_fields[i];
        let source_id = obj_names[i] + "-" + row_id;
        let form_elem = document.getElementById(form_elem_id);
        let next_form_elem = form_elem.nextElementSibling;

        form_elem.value = source_tr.children[source_id].innerText;

        if (next_form_elem && next_form_elem.hasAttribute("id") && next_form_elem.getAttribute("id") === form_elem_id) {
            next_form_elem.value = source_tr.children[source_id].innerText;
        }
    }
}
