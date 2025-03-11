function buscarLibros() {
    let termino = document.getElementById("busqueda").value;
    fetch(`/buscar?termino=${termino}`)
        .then(response => response.json())
        .then(data => {
            let resultados = document.getElementById("resultados");
            resultados.innerHTML = "";
            data.forEach(libro => {
                let item = document.createElement("li");
                item.classList.add("list-group-item");
                item.textContent = `${libro.Titulo} - ${libro.Autor} (${libro.Genero})`;
                resultados.appendChild(item);
            });
        });
}

function exportarExcel() {
    let fecha_inicio = document.getElementById("fecha_inicio").value;
    let fecha_fin = document.getElementById("fecha_fin").value;
    
    if (!fecha_inicio || !fecha_fin) {
        alert("Por favor, selecciona un rango de fechas.");
        return;
    }

    let formData = new FormData();
    formData.append("fecha_inicio", fecha_inicio);
    formData.append("fecha_fin", fecha_fin);

    fetch('/exportar', {
        method: "POST",
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        let link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "registros.xlsx";
        link.click();
    });
}
