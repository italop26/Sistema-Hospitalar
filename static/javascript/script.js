// ============================================================
// SISTEMA HOSPITALAR
// JAVASCRIPT
// MÓDULO: MÉDICO
// ============================================================


// ============================================================
// 1. MOSTRAR / OCULTAR SENHA
// ============================================================
//
// Classes utilizadas:
// .caixa-entrada
//
// Elementos utilizados:
// input[type="password"]
//
// Usado em:
// - login.html
// - confirmar_atendimento.html
//
// A ideia é reaproveitar a mesma função futuramente
// para Gestão e Paciente.
// ============================================================

function configurarVisibilidadeSenha() {

    const caixasSenha = document.querySelectorAll(
        ".caixa-entrada"
    );

    caixasSenha.forEach(function(caixa) {

        const input = caixa.querySelector(
            'input[type="password"], input[type="text"]'
        );

        if (!input) {
            return;
        }

        const botao = document.createElement("button");

        botao.type = "button";
        botao.textContent = "Mostrar";

        botao.className = "alternar-visibilidade";

        botao.addEventListener("click", function() {

            if (input.type === "password") {

                input.type = "text";

                botao.textContent = "Ocultar";

            } else {

                input.type = "password";

                botao.textContent = "Mostrar";

            }

        });

        caixa.appendChild(botao);

    });

}


// ============================================================
// 2. FEEDBACK AO ENVIAR FORMULÁRIO
// ============================================================
//
// Classes utilizadas:
// .formulario-secao
// .botao-primario
//
// Usado em:
// - atendimento_consulta.html
// - atendimento_exame.html
//
// O objetivo é evitar que o médico clique várias vezes
// enquanto o formulário está sendo enviado.
// ============================================================

function configurarEnvioFormulario() {

    const formularios = document.querySelectorAll(
        ".formulario-secao"
    );

    formularios.forEach(function(formulario) {

        formulario.addEventListener("submit", function() {

            const botao = formulario.querySelector(
                ".botao-primario"
            );

            if (!botao) {
                return;
            }

            botao.disabled = true;

            botao.textContent = "Enviando...";

        });

    });

}


// ============================================================
// 3. CONFIRMAÇÃO AO SAIR
// ============================================================
//
// Classe utilizada:
// .item-sair
//
// Usado no menu lateral do médico.
//
// Evita que o médico saia sem querer.
// ============================================================

function configurarSaida() {

    const itensSair = document.querySelectorAll(
        ".item-sair a"
    );

    itensSair.forEach(function(link) {

        link.addEventListener("click", function(event) {

            const confirmou = confirm(
                "Deseja realmente sair do sistema?"
            );

            if (!confirmou) {

                event.preventDefault();

            }

        });

    });

}


// ============================================================
// 4. CONFIRMAÇÃO AO VOLTAR DO ATENDIMENTO
// ============================================================
//
// Classe utilizada:
// .botao-secundario
//
// Usado em:
// - confirmar_atendimento.html
//
// Evita sair da confirmação sem perceber.
// ============================================================

function configurarBotaoVoltar() {

    const botoes = document.querySelectorAll(
        ".botao-secundario"
    );

    botoes.forEach(function(botao) {

        const texto = botao.textContent.trim().toLowerCase();

        if (texto !== "voltar") {
            return;
        }

        botao.addEventListener("click", function(event) {

            const confirmou = confirm(
                "Deseja voltar? As informações ainda não foram concluídas."
            );

            if (!confirmou) {

                event.preventDefault();

            }

        });

    });

}


// ============================================================
// 5. DESTAQUE DOS REGISTROS
// ============================================================
//
// Classe utilizada:
// .item-registro
//
// Usado em:
// - painel.html
//
// O CSS já possui :hover, então aqui não precisamos
// inventar outra classe. A interação é apenas complementar.
// ============================================================

function configurarRegistros() {

    const registros = document.querySelectorAll(
        ".item-registro"
    );

    registros.forEach(function(registro) {

        registro.addEventListener("click", function(event) {

            const link = registro.querySelector(
                "a"
            );

            // Se o médico clicar diretamente em um botão/link,
            // deixamos o comportamento normal acontecer.
            if (event.target.closest("a")) {
                return;
            }

            if (link) {
                link.focus();
            }

        });

    });

}


// ============================================================
// 6. CONFIRMAÇÃO DA FINALIZAÇÃO
// ============================================================
//
// Classe utilizada:
// .botao-primario
//
// Usado em:
// - confirmar_atendimento.html
//
// Antes de enviar a senha, confirma se o médico realmente
// deseja concluir o atendimento.
// ============================================================

function configurarConfirmacaoFinal() {

    const formularios = document.querySelectorAll(
        "form"
    );

    formularios.forEach(function(formulario) {

        const titulo = document.querySelector(
            "h1"
        );

        if (!titulo) {
            return;
        }

        const textoTitulo = titulo.textContent
            .trim()
            .toLowerCase();

        if (!textoTitulo.includes("confirmar atendimento")) {
            return;
        }

        formulario.addEventListener("submit", function(event) {

            const confirmou = confirm(
                "Deseja realmente confirmar e concluir este atendimento?"
            );

            if (!confirmou) {

                event.preventDefault();

                return;

            }

            const botao = formulario.querySelector(
                ".botao-primario"
            );

            if (botao) {

                botao.disabled = true;

                botao.textContent = "Confirmando...";

            }

        });

    });

}


// ============================================================
// 7. ANIMAÇÃO / ENTRADA
// ============================================================
//
// Classe utilizada:
// .fade
//
// O CSS já possui a animação.
//
// Aqui apenas garantimos que elementos marcados com .fade
// possam ser utilizados futuramente sem criar outra classe.
// ============================================================

function configurarFade() {

    const elementos = document.querySelectorAll(
        ".fade"
    );

    elementos.forEach(function(elemento) {

        elemento.style.opacity = "1";

    });

}


// ============================================================
// INICIALIZAÇÃO
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        configurarVisibilidadeSenha();

        configurarEnvioFormulario();

        configurarSaida();

        configurarBotaoVoltar();

        configurarRegistros();

        configurarConfirmacaoFinal();

        configurarFade();

    }
);