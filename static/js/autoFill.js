function autoFill(num, source) {
    const source_tr = document.getElementById(source).children[1].children[num - 1];
    const id_and_value = [
        ["id_wave_length", "wave-length-" + num],
        ["id_glasses_distance", "glasses-dist-" + num],
        ["id_focal_distance", "focal-distance-" + num],
        ["id_stroke_difference", "stroke-difference-" + num],
        ["id_reflectivity", "reflectivity-" + num],
        ["id_refractive_index", "refractive-index-" + num],
        ["id_picture_size", "picture-size-" + num],
        ["id_incident_light_intensity", "incident-light-intensive-" + num],
        ["id_N", "n-" + num]
    ]

    fillValues(source_tr, id_and_value);
}

function autoFillM(num, source) {
    const source_tr = document.getElementById(source).children[1].children[num - 1];
    const id_and_value = [
        ["id_wavelength", "wavelength-" + num],
        ["id_z1", "z1-" + num],
        ["id_z2", "z2-" + num],
        ["id_Rbs", "Rbs-" + num],
        ["id_tx", "tx-" + num],
        ["id_ty", "ty-" + num],
        ["id_f", "f-" + num],
        ["id_size", "size-" + num],
        ["id_N", "n-" + num]
    ]

    fillValues(source_tr, id_and_value);
}

function fillValues(source_tr, id_and_value) {
    for (let i in id_and_value) {
        document.getElementById(id_and_value[i][0]).value = source_tr.children[id_and_value[i][1]].innerText;

        let next_elem = document.getElementById(id_and_value[i][0]).nextElementSibling
        if (next_elem && next_elem.hasAttribute("id") && next_elem.getAttribute("id") === id_and_value[i][0]) {
            next_elem.value = source_tr.children[id_and_value[i][1]].innerText;
        }
    }
}
