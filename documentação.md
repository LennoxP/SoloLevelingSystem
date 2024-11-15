# Documentação do Projeto "Sistema de Estudo Gamificado"

## Descrição Geral
O projeto **Sistema de Estudo Gamificado** é uma aplicação desenvolvida em Python usando a biblioteca Tkinter, que incentiva o aprendizado por meio de uma estrutura gamificada. O usuário pode completar tarefas diárias de estudo em diferentes linguagens de programação e tópicos de aprendizado de máquina, ganhando experiência e subindo de nível conforme progride.

## Estrutura de Arquivos e Classes

### Classes Principais
O sistema é baseado em três classes principais:

1. **Estudante**: Representa o aluno, com atributos e métodos relacionados ao progresso, como `completar_tarefa`, `subir_de_nivel` e `salvar_progresso`.
2. **SistemaEstudo**: Responsável por gerenciar as tarefas diárias e escolher tarefas apropriadas para o nível do estudante.
3. **GUI**: Interface gráfica que exibe o status do estudante, tarefas diárias e exibe notificações visuais quando uma tarefa é concluída ou o estudante sobe de nível.

### Estrutura de Arquivos
- **`main.py`**: Contém o código principal com a definição das classes e inicialização da aplicação.
- **`progresso.json`**: Arquivo JSON que armazena o progresso do usuário entre as sessões.

## Descrição dos Principais Componentes

### 1. Classe `Estudante`
Representa o usuário e gerencia seu progresso:
- **Atributos**: `nivel`, `experiencia`, `tarefas_completas`, `total_tarefas`, `total_experiencia`.
- **Métodos Principais**:
    - **completar_tarefa**: Adiciona pontos de experiência e incrementa a contagem de tarefas concluídas. Se o estudante atingir 100 pontos de experiência, ele sobe de nível.
    - **subir_de_nivel**: Aumenta o nível do estudante, reinicia a experiência e exibe uma mensagem de congratulação.
    - **salvar_progresso** e **carregar_progresso**: Salva e recupera os dados do estudante em um arquivo JSON para manter o progresso entre as sessões&#8203;:contentReference[oaicite:0]{index=0}.

### 2. Classe `SistemaEstudo`
Gerencia as tarefas diárias:
- **Atributos**:
    - **linguagens**: Dicionário de tópicos organizados por linguagem e nível de dificuldade (inicial e avançado).
    - **tarefas_diarias**: Lista de tarefas geradas para o estudante.
- **Métodos Principais**:
    - **gerar_tarefas_diarias**: Gera quatro tarefas diárias baseadas no nível do estudante. Estudantes de nível 50 ou superior recebem tarefas avançadas.
    - **obter_tarefas_diarias**: Retorna a lista de tarefas diárias geradas&#8203;:contentReference[oaicite:1]{index=1}.

### 3. Classe `GUI`
Define a interface gráfica do sistema e gerencia a interação do usuário:
- **Elementos Principais**:
    - **Botões**: Inclui botões para gerar tarefas diárias, mostrar o status do usuário e redefinir o progresso.
    - **Exibição de Tarefas**: Exibe as tarefas diárias em uma lista. Cada tarefa pode ser marcada como concluída, o que concede pontos de experiência ao usuário.
- **Métodos Principais**:
    - **atualizar_tarefas**: Atualiza a lista de tarefas diárias exibidas na interface.
    - **concluir_tarefa**: Registra a conclusão de uma tarefa e exibe um popup de missão concluída.
    - **mostrar_status_janela**: Exibe o status completo do estudante em uma janela popup.
    - **confirmar_resetar_progresso**: Confirma a redefinição do progresso do estudante com uma notificação popup&#8203;:contentReference[oaicite:2]{index=2}.

## Funcionalidades

- **Progresso e Níveis**: O estudante ganha pontos de experiência completando tarefas e sobe de nível a cada 100 pontos.
- **Tarefas Diárias Personalizadas**: Gera tarefas de acordo com o nível de experiência do estudante, permitindo um progresso constante.
- **Interface Visual Interativa**: A interface gráfica permite fácil interação e fornece feedback visual por meio de janelas popup de congratulação.
- **Salvar e Recuperar Progresso**: Salva automaticamente o progresso para garantir que o usuário não perca dados entre sessões.

## Tecnologias Utilizadas
- **Python**: Linguagem principal para a lógica do sistema.
- **Tkinter**: Usado para a construção da interface gráfica.
- **JSON**: Armazenamento persistente de dados para salvar o progresso do estudante.

---

Este projeto proporciona uma estrutura para um sistema de aprendizado gamificado, ideal para aprendizado interativo em diversas áreas. Ele permite que o usuário experimente uma sensação de progresso e realização enquanto adquire novas habilidades.
