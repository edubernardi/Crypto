# Trabalho 3

## Objetivo
Este trabalho tem como objetivo encriptar e decriptar arquivos lidos por blocos(6 bits por vez).

---

A função <span style="color:green; font-weight:700">encrypt</span> recebe 2 parâmetros, <span style="color:orange">input_file</span> e <span style="color:orange">key</span>.
A função <span style="color:green; font-weight:700">decrypt</span> recebe 2 parâmetros, <span style="color:orange">input_file</span> e <span style="color:orange">key</span>. A diferença é na hora de gerar a <span style="color:orange">key</span> e realizar a <span style="color:brown; font-weight:700">substitution</span>, que são invertidas!
A função <span style="color:green; font-weight:700">key_schedule</span> recebe 2 parâmetros, <span style="color:orange">key</span> e <span style="color:orange">round</span>. Esta função retorna uma chave diferente por <span style="color:purple">round</span> baseada em <span style="color:#f43f5e">fibonacci</span>.

- Para criptografar, é definido um número de <span style="color:purple">rounds</span> que ocorrerão, nós escolhemos *15*.
- Para cada <span style="color:purple">round</span>, é gerada uma nova <span style="color:orange">key</span> e essa <span style="color:orange">key</span> é loopada e cada bit recebe seu número correspondente na tabela *ASCII*, para tornar mais difícil a quebra da criptografia.
- Logo em seguida, é aplicada a <span style="color:blue; font-weight:700">Caesar Cipher</span> em cada bit da <span style="color:orange">key</span>, onde o índice de ciframento é o próprio <span style="color:purple">round</span>.
- O próximo passo é realizar um <span style="color:red; font-weight:700">XOR</span> entre as posições i do <span style="color:orange">input_file</span> e da <span style="color:orange">key</span>.
- Com o resultado deste <span style="color:red; font-weight:700">XOR</span>, é realizado uma <span style="color:brown; font-weight:700">substitution</span>, que é uma função que transforma os bits para decimal e realiza uma substituição de linhas e colunas
- Para finalizar, é retirado o padding e o arquivo <span style="color:green; font-weight:700">Criptografado</span> é escrito!
