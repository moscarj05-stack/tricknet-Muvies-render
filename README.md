# TrickNet Render

Fábrica de vídeos do canal **TrickNet Aprenda**: renderiza cenas 3D com o Blender no GitHub Actions
(várias partes em paralelo) e monta o vídeo final nas versões **horizontal (16:9)** e **vertical (9:16)**.

## Estrutura
- `cenas/etapa1/cena.py` – a cena 3D da Etapa 1 (casa em corte, caixa-d'água, manômetro, mascote).
- `cenas/etapa1/config.json` – tamanho, quadros e legendas de cada formato.
- `lib/tricknet_lib.py` – materiais, cores e o mascote TrickNet.
- `ferramentas/plano.py` – divide a cena em partes para renderizar em paralelo.
- `ferramentas/montar.py` – junta os quadros em MP4 e coloca as legendas.
- `.github/workflows/render.yml` – o fluxo que roda tudo (criado à parte, veja o passo 4).

## Passo a passo
1. Crie uma conta grátis em github.com e confirme o e-mail.
2. Clique em **+ → New repository**. Nome: `tricknet-render`. Marque **Public**. Clique em **Create repository**.
3. Na página do repositório, clique em **uploading an existing file** e arraste para lá **o conteúdo** desta pasta
   (as pastas `cenas`, `ferramentas`, `lib` e o `README.md`). Clique em **Commit changes**.
4. Clique em **Add file → Create new file**. No campo do nome digite exatamente `.github/workflows/render.yml`
   (as barras criam as pastas). Cole o conteúdo do arquivo `render.yml` e clique em **Commit changes**.
5. Abra a aba **Actions → Renderizar cena → Run workflow**.
   Para o primeiro teste use resolução `0.5` e amostras `16` (rápido). Clique em **Run workflow**.
6. Quando terminar (✓ verde), abra a execução e, no fim da página, em **Artifacts**, baixe `videos-etapa1`.
   Dentro estão `etapa1_horizontal.mp4` e `etapa1_vertical.mp4`.
7. Para a qualidade final, rode de novo com resolução `1.0` e amostras `48` (ou `96`).

## Observações
- Repositório **público** tem minutos grátis ilimitados. Não coloque senhas nem chaves nos arquivos.
- Se aparecer um ✗ vermelho, abra o passo que falhou, copie as últimas linhas do log e envie para o Claude.
