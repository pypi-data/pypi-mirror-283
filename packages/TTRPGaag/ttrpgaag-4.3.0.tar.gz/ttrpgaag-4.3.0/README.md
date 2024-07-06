# RPG
Pacote Python com as minhas ferramentas de RPG

- **4.3.0** - DC20. Inclusão do rolamento para ataques
- **4.2.0** - DC20. Classe para realizar rolamentos
- **4.1.1** - Novas funcionalidades em Dado:
  - Função de abertura privada no Dado (`_reiniciar`), para usos específicos como chamar a classe com número de dados ou faces variados (exemplo: o dado pode aumentar a face, a quantidade pode ser acrescida de um dado)
  - Propriedade `rolamento` para exibir os dados rolados
- **4.1.0** - Nova classe para tabelas roláveis `TabelaRolavelSimples` para tabelas que cada item tem a mesma chance de sair (como 20 itens e rolar d20)
- **4.0.1** - Atualização das importações usando caminho relativo
- **4.0.0** - Métodos de criação de tabelas da `TabelaRolavel` renomeados para o verbo no infinitivo. Inclusão de parâmetro para rolar a subtabela ou não
- **3.0.3** - `TabelaRolavel` agora aceita e rola o resultado de outra tabela caso esse seja o resultado. Por exemplo: a tabela de tesouro pode fazer rolar na tabela de armas mágicas. Se cair esse resultado, já vai entregar o devido resultado
- **3.0.2** - `rolar_tabela` agora usa prioritariamente dicionário
- **3.0.1** - Otimização no embaralhamento de cartas, usando função nativa do módulo random
- **3.0.0** - PF2
  - Alteração do parâmetro `.defesa_base` para `.defesa_monstro_base` para deixar mais claro seu uso
  - Alteração do import do módulo `calcula_proficiencia` para `proficiencia` pois ganhou outra função: `aumentar_proficiencia` 
  - Lista de skills em Data
  - Classe de PC para representar um personagem
- **2.2.3** - Inclusão dos danos só de rolamento no PF2
- **2.2.2** - Inclusão de valor do ataque do ataque atual como propriedade em PF2
- **2.2.1** - Correção no cálculo de save do PF2
- **2.2.0** - Inclusão do submódulo de pf2
- **2.1.2** - Correção na representação de dado
- **2.1.0** - Correção de bug
- **2.0.0** - Alteração na classe Baralho
- **1.0.0** - Lançamento