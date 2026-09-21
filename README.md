# 🏥 MedAgenda — Sistema de Gestão Clínica
Sistema web desenvolvido em **Django** para gerenciamento de uma clínica, com diferentes fluxos para pacientes, médicos e gestão.
O projeto foi desenvolvido com foco em prática de **backend, APIs, banco de dados, autenticação, regras de negócio e integração entre diferentes perfis de usuário**.

---

## 🚀 Funcionalidades

### 👤 Paciente

* Cadastro e autenticação
* Visualização do perfil
* Solicitação de consultas
* Visualização de consultas agendadas
* Histórico de consultas
* Visualização de resultados de exames
* Acompanhamento dos atendimentos

### 👨‍⚕️ Médico

* Autenticação utilizando CRM
* Visualização de atendimentos
* Separação entre vagas de consultas e exames
* Registro do atendimento médico
* Registro de diagnóstico, conduta e prescrição
* Finalização de consultas e exames

### 🏥 Gestão

* Controle geral da clínica
* Gerenciamento de médicos e vagas
* Acompanhamento de consultas e exames
* Controle dos fluxos de atendimento

## 📌 Funcionalidades principais

O sistema possui diferentes níveis de acesso e fluxos de acordo com o perfil do usuário.

* **Paciente:** pode solicitar consultas, acompanhar agendamentos, acessar seu histórico, resultados de exames e informações dos atendimentos.
* **Médico:** realiza atendimentos, registra diagnóstico, conduta, prescrição e pode emitir receitas vinculadas à consulta.
* **Gestão:** possui controle geral do sistema, podendo cadastrar e gerenciar médicos, horários, vagas, consultas e exames.
* **Consultas e exames:** possuem fluxos próprios de agendamento, atendimento, conclusão e disponibilização dos resultados.
* **Receitas:** são registradas durante o atendimento médico e ficam vinculadas ao atendimento do paciente. Que podem ser baixadas em pdf

🔌 API

O sistema também possui uma API desenvolvida com Django REST Framework, responsável por parte da lógica de agendamento e comunicação entre os dados da aplicação.

A API participa do fluxo de solicitação de consultas, realizando o processamento necessário para verificar a disponibilidade e selecionar um médico de acordo com as regras definidas no sistema.

Isso permite separar parte da regra de negócio do sistema da camada de interface, tornando o fluxo mais organizado e possibilitando que diferentes partes da aplicação consumam esses recursos.

## 📸 Demonstração

### 🔐 Login

Tela inicial de autenticação dos usuários.

<img width="1600" height="900" alt="login_paciente" src="https://github.com/user-attachments/assets/cae519be-e82d-4d0a-9b19-3ec7f45a536a" />


---

### 👤 Tela do paciente

Área principal do paciente, contendo informações do perfil e seus agendamentos.

<img width="1594" height="728" alt="parte_principal_paciente" src="https://github.com/user-attachments/assets/a127be63-c772-4276-804d-a4de68e132ad" />


---

### 📅 Solicitação de consulta

Fluxo utilizado pelo paciente para solicitar uma consulta de acordo com a disponibilidade do sistema.

![Solicitação de consulta]<img width="1594" height="728" alt="Marcação" src="https://github.com/user-attachments/assets/a240cbc0-595e-4667-a8c3-f59315028cc2" />


---

### 👨‍⚕️ Tela do médico

Área do médico com as vagas disponíveis, separadas entre consultas e exames, além dos atendimentos.

![Tela do médico]<img width="1594" height="728" alt="painel_medico" src="https://github.com/user-attachments/assets/65631e4f-f606-4101-9c56-e4fb541e991a" />


---

### 🩺 Atendimento médico

Tela utilizada durante o atendimento para registrar informações como queixa, sintomas, diagnóstico, conduta e prescrição.

![Atendimento médico]<img width="1594" height="728" alt="atendimento medico" src="https://github.com/user-attachments/assets/a42a581a-b39e-425a-9b30-6c62b180e1f1" />


---

### 📋 Histórico e resultados

Visualização do histórico de atendimentos e dos resultados de exames após sua conclusão. Para o paciente ver suas consultas/exames feitas

![Histórico e resultados]<img width="1594" height="728" alt="Code_JssfsDieoa" src="https://github.com/user-attachments/assets/06db35cd-07b3-4dfa-ac54-03c1e7c12663" />



---

### 🏥 Gestão da clínica

Área destinada ao controle geral dos fluxos da clínica. Onde fica o controle central do sistema

<img width="1594" height="728" alt="Gestão" src="https://github.com/user-attachments/assets/fd3e69c2-da7e-4e1a-9b48-5d2fde37e245" />


---

## 🛠️ Tecnologias utilizadas

* **Python**
* **Django**
* **Django REST Framework**
* **JavaScript**
* **HTML5**
* **CSS3**
* **SQL**
* **MYSQL**
* **Git / GitHub**

---

## 🧠 Principais conceitos praticados

* Arquitetura de aplicações Django
* Modelagem de banco de dados
* Relacionamentos entre modelos
* Autenticação e autorização
* Controle de acesso por perfil
* APIs REST
* Regras de negócio
* Views e templates
* Formulários
* Integração entre frontend e backend
* JavaScript para interatividade
* Validação e tratamento de dados
* Organização de código
* Versionamento com Git

---

## 🔄 Fluxo principal
<img width="1600" height="900" alt="login_paciente" src="https://github.com/user-attachments/assets/b6edd509-2d7a-402b-897b-7c0104b2aac5" />

Paciente
   ↓
Solicita consulta
   ↓
Sistema verifica disponibilidade
   ↓
Consulta é agendada
   ↓
Médico realiza o atendimento
   ↓
Registro do atendimento
   ↓
Diagnóstico / Conduta / Prescrição
   ↓
Consulta finalizada
   ↓
Paciente acessa seu histórico
```

Para exames, o fluxo segue uma lógica semelhante, com o resultado sendo disponibilizado ao paciente após a conclusão do exame.

> ⚠️ **Atenção**
>
> O projeto está em fase final de desenvolvimento e ainda possui alguns detalhes como segurança dos dados e melhorias que serão adicionados posteriormente. Mas o sistema em si já está pronto, porém faltas detalhes que falta para finalizar 100% do sistema



## 📌 Sobre o projeto

O **MedAgenda** foi desenvolvido como projeto de portfólio para colocar em prática conhecimentos de desenvolvimento web com Python e Django, principalmente na construção de sistemas com múltiplos perfis de usuário, regras de negócio, banco de dados e APIs.
O projeto também serviu como prática para desenvolvimento e organização de uma aplicação completa, desde os modelos e regras do backend até as interfaces utilizadas pelos diferentes usuários.

