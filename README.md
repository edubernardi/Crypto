# Teoria da Informação - Trabalho 4: Cifrador Simétrico de Bloco

## Objetivo
Este trabalho tem como objetivo criptografar e decriptar arquivos lidos por blocos (6 bytes por vez).

---

Através de argumentos da linha de comando, são passados o nome do arquivo e a chave para criptografia, no formato "crypto.py {input file} {key (4 bytes long)}"
Caso o arquivo possua ".crypto", será chamada a função <span style="color:green; font-weight:700">decrypt</span>, que vai decriptar a entrada e gerar um arquivo ".decrypt" como saída.
Caso contrário, <span style="color:green; font-weight:700">encrpy</span> será chamada e a saída será um arquivo ".crypto".
A chave fornecida deve ser de 4 bytes. Se for maior, apenas os primeiros 4 serão considerados. Se for menor, a função retorna e não é executada.
Ambas as funções <span style="color:green; font-weight:700">encrypt</span>  e <span style="color:green; font-weight:700">decrypt</span> recebem 2 parâmetros, <span style="color:orange">input_file</span> e <span style="color:orange">key</span>. A diferença da função de criptografia se da no processo de <span style="color:orange">key scheduling</span>, pois nesse caso as chaves são consumidas na ordem reversa. O restante das operações também é realizado na ordem inversa para descriptografia.
É lido um bloco de 6 bytes a cada iteração, o arquivo esteja no fim e não for possível ler 6 bytes, é realizado o padding com bytes null.
O processo de criptografia se dá através de rounds, a cada um é executado o <span style="color:green; font-weight:700">key_schedule</span> e as operações de Cifra de César, XOR e Substituição.
- A função <span style="color:green; font-weight:700">key_schedule</span> recebe 2 parâmetros, <span style="color:orange">key</span> e <span style="color:orange">round</span>. Esta função retorna uma chave diferente por <span style="color:purple">round</span> baseada <span style="color:#f43f5e">na sequencia fibonacci</span> e na chave anterior.
- A Cifra de César adiciona para cada byte da chave o indíce do round atual.
- A operação XOR é realizada bit a bit, entre cada bit da chave e do bloco atual.
- O processo de substituição é feito a partir de uma s_box 4x4. Para a decriptografia é utilizada uma s_box invertida.
- O número de rounds usados na criptografia e descriptografia deve ser o mesmo, para execução foram definidos como *15*.
Como último passo, na função <span style="color:green; font-weight:700">decrypt</span> é realizado a aremoção do padding, os bytes nulos ao final do arquivo.
