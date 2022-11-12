function autoFill(num, source) {
    const source_tr = document.getElementById(source).children[1].children[num - 1];

    document.getElementById("id_wave_length").value = source_tr.children["wave-length-" + num].innerText;
    document.getElementById("id_glasses_distance").value = source_tr.children["glasses-dist-" + num].innerText;
    document.getElementById("id_focal_distance").value = source_tr.children["focal-distance-" + num].innerText;
    document.getElementById("id_stroke_difference").value = source_tr.children["stroke-difference-" + num].innerText;
    document.getElementById("id_reflectivity").value = source_tr.children["reflectivity-" + num].innerText;
    document.getElementById("id_refractive_index").value = source_tr.children["refractive-index-" + num].innerText;
    document.getElementById("id_picture_size").value = source_tr.children["picture-size-" + num].innerText;
    document.getElementById("id_incident_light_intensity").value = source_tr.children["incident-light-intensive-" + num].innerText;
    document.getElementById("id_N").value = source_tr.children["n-" + num].innerText;
}

function autoFillM(num, source) {
    const source_tr = document.getElementById(source).children[1].children[num - 1];

    document.getElementById("id_wavelength").value = source_tr.children["wavelength-" + num].innerText;
    document.getElementById("id_z1").value = source_tr.children["z1-" + num].innerText;
    document.getElementById("id_z2").value = source_tr.children["z2-" + num].innerText;
    document.getElementById("id_Rbs").value = source_tr.children["Rbs-" + num].innerText;
    document.getElementById("id_tx").value = source_tr.children["tx-" + num].innerText;
    document.getElementById("id_ty").value = source_tr.children["ty-" + num].innerText;
    document.getElementById("id_f").value = source_tr.children["f-" + num].innerText;
    document.getElementById("id_size").value = source_tr.children["size-" + num].innerText;
    document.getElementById("id_N").value = source_tr.children["n-" + num].innerText;
}