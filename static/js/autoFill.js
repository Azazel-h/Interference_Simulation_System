function autoFill(num) {
    document.getElementById("id_laser_color").value = document.getElementById("laser-color-" + num).className;
    document.getElementById("id_glasses_distance").value = document.getElementById("glasses-dist-" + num).innerText;
    document.getElementById("id_focal_distance").value = document.getElementById("focal-distance-" + num).innerText;
    document.getElementById("id_stroke_difference").value = document.getElementById("stroke-difference-" + num).innerText;
    document.getElementById("id_reflectivity").value = document.getElementById("reflectivity-" + num).innerText;
    document.getElementById("id_refractive_index").value = document.getElementById("refractive-index-" + num).innerText;
    document.getElementById("id_picture_size").value = document.getElementById("picture-size-" + num).innerText;
    document.getElementById("id_incident_light_intensity").value = document.getElementById("incident-light-intensive-" + num).innerText;
    document.getElementById("id_N").value = document.getElementById("n-" + num).innerText;
}