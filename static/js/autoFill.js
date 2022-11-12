function autoFill(num) {
    document.getElementById("id_wave_length").value = document.getElementById("wave-length-" + num).innerText;
    document.getElementById("id_glasses_distance").value = document.getElementById("glasses-dist-" + num).innerText;
    document.getElementById("id_focal_distance").value = document.getElementById("focal-distance-" + num).innerText;
    document.getElementById("id_stroke_difference").value = document.getElementById("stroke-difference-" + num).innerText;
    document.getElementById("id_reflectivity").value = document.getElementById("reflectivity-" + num).innerText;
    document.getElementById("id_refractive_index").value = document.getElementById("refractive-index-" + num).innerText;
    document.getElementById("id_picture_size").value = document.getElementById("picture-size-" + num).innerText;
    document.getElementById("id_incident_light_intensity").value = document.getElementById("incident-light-intensive-" + num).innerText;
    document.getElementById("id_N").value = document.getElementById("n-" + num).innerText;
}

function autoFillM(num) {
    document.getElementById("id_wavelength").value = document.getElementById("wavelength-" + num).innerText;
    document.getElementById("id_z1").value = document.getElementById("z1-" + num).innerText;
    document.getElementById("id_z2").value = document.getElementById("z2-" + num).innerText;
    document.getElementById("id_Rbs").value = document.getElementById("Rbs-" + num).innerText;
    document.getElementById("id_tx").value = document.getElementById("tx-" + num).innerText;
    document.getElementById("id_ty").value = document.getElementById("ty-" + num).innerText;
    document.getElementById("id_f").value = document.getElementById("f-" + num).innerText;
    document.getElementById("id_size").value = document.getElementById("size-" + num).innerText;
    document.getElementById("id_N").value = document.getElementById("n-" + num).innerText;
}