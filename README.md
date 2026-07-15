Visão geral do projeto
É um software que visa ser usado como um programa de estoque de quantidade de livros (com informações como : nome, autor, quantidade, ID de listagem) e ainda com um sistema de empréstimo de livros (como aquelas bibliotecas públicas de município, por exemplo, em que os livros são de livre acesso).

Funcionalidades (O CRUD)
Cadastramento do livro : Nome, autor
Edição de informações do livro 
Contagem de quantidade de livros disponíveis
Registro de empréstimo : Data em que o empréstimo foi feito, Nome e CPF de quem pegou o livro emprestado ;

 Estrutura de Dados e Persistência
Manipulação em Memória: Os dados do sistema são manipulados em tempo de execução utilizando uma estrutura de dicionário principal contendo listas de dicionários (uma lista para "livros" e outra para "emprestimos"). 

Cada livro e cada empréstimo é representado como um dicionário Python (com chaves como id, titulo, nome_pessoa, etc.), o que permite o acesso, atualização e remoção rápida e nativa dos atributos diretamente na memória do computador.  

Persistência de Dados: Para que as informações não sejam perdidas ao fechar o programa, os dados são persistidos utilizando o formato JSON (JavaScript Object Notation), gravados no arquivo local livros.json. Escolheu-se o JSON por ser um formato estruturado, amplamente utilizado no mercado, de fácil leitura tanto para humanos quanto para sistemas, e que se integra nativamente com as estruturas de dicionários e listas do Python através da biblioteca padrão.
Instruções de Uso

Pré-requisitos e Dependências: O sistema foi desenvolvido utilizando exclusivamente as bibliotecas nativas do Python (tkinter, json, os e datetime). Portanto, não há necessidade de instalar nenhuma dependência extra via PIP. Basta ter o Python instalado na máquina (versão 3.x recomendada).  

Como Baixar/Clonar o Projeto:Baixe o arquivo Estoque.py diretamente para o  computador (ou clone o repositório do projeto, caso utilize Git).Certifique-se de salvar o arquivo em uma pasta dedicada de sua preferência.Como Executar o Programa:Abir o terminal do seu sistema operacional (ou o terminal integrado do VS Code) e navegar até a pasta onde o arquivo foi salvo.

Execute o seguinte comando para iniciar a interface do sistema: python Estoque.py

O programa abrirá a tela principal automaticamente e criará o arquivo “livros.json”  na mesma pasta assim que qualquer dado for salvo.
