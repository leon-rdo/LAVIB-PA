function escreverTexto(elemento, texto) {
    let i = 0;
    function escrever() {
        if (i < texto.length) {
            elemento.innerHTML += texto.charAt(i);
            i++;
            setTimeout(escrever, 50);
        }
    }
    escrever();
}

const textoAnimado = document.getElementById("title");
const texto = "- Liga Acadêmica de Virologia e Bacteriologia do Pará -";
escreverTexto(textoAnimado, texto);