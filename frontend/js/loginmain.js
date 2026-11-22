// Efecto de las etiquetas al enfocar los campos.
const inputs = document.querySelectorAll(".input");

function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}

inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});

// Ingreso y panel de documentos.
const formulario = document.getElementById("form-ingreso");
const mensaje = document.getElementById("mensaje");
const panel = document.getElementById("panel");
const saludo = document.getElementById("saludo");
const resumen = document.getElementById("resumen");
const filas = document.getElementById("documentos");

const ETIQUETAS = { vencido: "Vencido", por_vencer: "Por vencer", vigente: "Vigente" };

function plural(dias){
	return dias === 1 ? "1 día" : dias + " días";
}

function detalle(documento){
	const dias = documento.dias_restantes;
	if(dias < 0) return "hace " + plural(-dias);
	if(dias === 0) return "vence hoy";
	return "faltan " + plural(dias);
}

function celda(texto, nota){
	const td = document.createElement("td");
	td.textContent = texto;
	if(nota){
		const pequeno = document.createElement("small");
		pequeno.textContent = nota;
		td.appendChild(pequeno);
	}
	return td;
}

function pintarDocumentos(documentos){
	filas.replaceChildren();
	documentos
		.slice()
		.sort((a, b) => a.dias_restantes - b.dias_restantes)
		.forEach(documento => {
			const fila = document.createElement("tr");
			fila.appendChild(celda(documento.name_document, documento.descripcion));
			fila.appendChild(celda(documento.expiracion, detalle(documento)));

			const estado = document.createElement("span");
			estado.className = "estado " + documento.estado;
			estado.textContent = ETIQUETAS[documento.estado] || documento.estado;
			const td = document.createElement("td");
			td.appendChild(estado);
			fila.appendChild(td);

			filas.appendChild(fila);
		});

	const porAtender = documentos.filter(d => d.estado !== "vigente").length;
	resumen.textContent = documentos.length === 0
		? "Todavía no tienes documentos registrados."
		: porAtender === 0
			? "Todos tus documentos están vigentes."
			: "Documentos que requieren atención: " + porAtender + " de " + documentos.length + ".";
}

async function pedir(ruta, opciones){
	let respuesta;
	try{
		respuesta = await fetch(ruta, opciones);
	}catch(error){
		throw new Error("No se pudo conectar con el servidor.");
	}
	const cuerpo = await respuesta.json().catch(() => null);
	if(!respuesta.ok){
		const detalleError = cuerpo && typeof cuerpo.detail === "string" ? cuerpo.detail : "No se pudo completar la solicitud.";
		throw new Error(detalleError);
	}
	return cuerpo;
}

formulario.addEventListener("submit", async evento => {
	evento.preventDefault();
	mensaje.textContent = "";

	const username = document.getElementById("usuario").value.trim();
	const password = document.getElementById("clave").value;

	try{
		const ingreso = await pedir("/login", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ username, password }),
		});
		const usuario = await pedir("/users/" + encodeURIComponent(ingreso.username));

		saludo.textContent = "Hola, " + ingreso.name;
		pintarDocumentos(usuario.documentss);
		formulario.hidden = true;
		panel.hidden = false;
	}catch(error){
		mensaje.textContent = error.message;
	}
});

document.getElementById("salir").addEventListener("click", () => {
	panel.hidden = true;
	formulario.hidden = false;
	formulario.reset();
	inputs.forEach(input => input.parentNode.parentNode.classList.remove("focus"));
});
