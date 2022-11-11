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