"""i18n.py — Sistema de internacionalização para Project Horse.
Idiomas: pt (Português), en (English), es (Español).
Uso: from i18n import T, set_lang, get_lang
"""

_LANG = 'pt'   # idioma ativo

# ── Dicionário de traduções ────────────────────────────────────────────────────
_TR = {
    # ── MENU PRINCIPAL ─────────────────────────────────────────────────────────
    'menu_corrida':          {'pt':'INICIAR CORRIDA',      'en':'START RACE',         'es':'INICIAR CARRERA'},
    'menu_cavalos':          {'pt':'Meus Cavalos',         'en':'My Horses',           'es':'Mis Caballos'},
    'menu_mercado':          {'pt':'Mercado',              'en':'Market',              'es':'Mercado'},
    'menu_patrocinador':     {'pt':'Patrocinadores',       'en':'Sponsors',            'es':'Patrocinadores'},
    'menu_banco':            {'pt':'Banco',                'en':'Bank',                'es':'Banco'},
    'menu_genealogia':       {'pt':'Genealogia',           'en':'Genealogy',           'es':'Genealogia'},
    'menu_cruzamento':       {'pt':'Cruzamento',           'en':'Breeding',            'es':'Cruza'},
    'menu_historico':        {'pt':'Historico',            'en':'History',             'es':'Historial'},
    'menu_calendario':       {'pt':'Calendario',           'en':'Calendar',            'es':'Calendario'},
    'menu_apostas':          {'pt':'Apostas',              'en':'Bets',                'es':'Apuestas'},
    'menu_funcionarios':     {'pt':'Funcionarios',         'en':'Staff',               'es':'Empleados'},
    'menu_trofeus':          {'pt':'Galeria Trofeus',      'en':'Trophy Gallery',      'es':'Galeria Trofeos'},
    'menu_config':           {'pt':'Configuracoes',        'en':'Settings',            'es':'Configuracion'},
    'menu_salvar':           {'pt':'Salvar',               'en':'Save',                'es':'Guardar'},
    'menu_carregar':         {'pt':'Carregar',             'en':'Load',                'es':'Cargar'},
    'menu_sair':             {'pt':'Sair',                 'en':'Exit',                'es':'Salir'},
    'menu_leilao':           {'pt':'Leilao',               'en':'Auction',             'es':'Subasta'},
    
    # ── NAVEGAÇÃO ──────────────────────────────────────────────────────────────
    'voltar':                {'pt':'Voltar',               'en':'Back',                'es':'Volver'},
    'ok':                    {'pt':'OK',                   'en':'OK',                  'es':'Aceptar'},
    'cancelar':              {'pt':'Cancelar',             'en':'Cancel',              'es':'Cancelar'},
    'confirmar':             {'pt':'Confirmar',            'en':'Confirm',             'es':'Confirmar'},
    'continuar':             {'pt':'Continuar',            'en':'Continue',            'es':'Continuar'},
    'proximo':               {'pt':'Proximo',              'en':'Next',                'es':'Siguiente'},
    'anterior':              {'pt':'Anterior',             'en':'Previous',            'es':'Anterior'},
    
    # ── COMPETIÇÃO ─────────────────────────────────────────────────────────────
    'competicao':            {'pt':'Escolha uma Competicao:','en':'Choose Competition:','es':'Elige Competicion:'},
    'sem':                   {'pt':'Semana',               'en':'Week',                'es':'Semana'},
    'semanas':               {'pt':'semanas',              'en':'weeks',               'es':'semanas'},
    'temporada':             {'pt':'Temporada',            'en':'Season',              'es':'Temporada'},
    'correndo_agora':        {'pt':'Correndo agora:',      'en':'Now racing:',         'es':'Corriendo ahora:'},
    'escala':                {'pt':'Escala:',              'en':'Lineup:',             'es':'Escalada:'},
    'premios':               {'pt':'Premios:',             'en':'Prizes:',             'es':'Premios:'},
    'nenhum_apto':           {'pt':'Nenhum cavalo apto esta semana!','en':'No eligible horse this week!','es':'Sin caballo apto esta semana!'},
    'corrida_btn':           {'pt':'CORRIDA!',             'en':'RACE!',               'es':'CARRERA!'},
    
    # ── CAVALOS ────────────────────────────────────────────────────────────────
    'meus_cavalos':          {'pt':'Meus Cavalos',         'en':'My Horses',           'es':'Mis Caballos'},
    'baias':                 {'pt':'Baias:',               'en':'Stalls:',             'es':'Establos:'},
    'manutencao':            {'pt':'Manut:',               'en':'Maint:',              'es':'Mant:'},
    'manutencao_semanal':    {'pt':'Manutencao Semanal',   'en':'Weekly Maintenance',  'es':'Mantenimiento Semanal'},
    'nenhum_cavalo':         {'pt':'Nenhum cavalo no haras.','en':'No horses in the stable.','es':'Sin caballos en el haras.'},
    'vender':                {'pt':'Vender',               'en':'Sell',                'es':'Vender'},
    'comprar':               {'pt':'Comprar',              'en':'Buy',                 'es':'Comprar'},
    'energia':               {'pt':'Energia',              'en':'Energy',              'es':'Energia'},
    'energia_full':          {'pt':'Energia Completa',     'en':'Full Energy',         'es':'Energia Completa'},
    'potro_falta':           {'pt':'Potro — pode correr em','en':'Foal — can race in', 'es':'Potro — puede correr en'},
    'vel':                   {'pt':'Vel',                  'en':'Spd',                 'es':'Vel'},
    'velocidade':            {'pt':'Velocidade',           'en':'Speed',               'es':'Velocidad'},
    'saude':                 {'pt':'Saude',                'en':'Health',              'es':'Salud'},
    'stamina':               {'pt':'Stamp',                'en':'Stamina',             'es':'Resistencia'},
    'vitorias':              {'pt':'Vit.',                 'en':'Wins',                'es':'Victorias'},
    'mant_label':            {'pt':'Mant.',                'en':'Maint.',              'es':'Mant.'},
    'rev_mercado':           {'pt':'Revenda:',             'en':'Resale:',             'es':'Reventa:'},
    'val_mercado':           {'pt':'Valor de mercado:',    'en':'Market value:',       'es':'Valor de mercado:'},
    'idade':                 {'pt':'Idade:',               'en':'Age:',                'es':'Edad:'},
    'raca':                  {'pt':'Raca:',                'en':'Breed:',              'es':'Raza:'},
    'cor':                   {'pt':'Cor:',                 'en':'Color:',              'es':'Color:'},
    'sexo':                  {'pt':'Sexo:',                'en':'Sex:',                'es':'Sexo:'},
    'historico':             {'pt':'Historico:',           'en':'History:',            'es':'Historial:'},
    'estrelas':              {'pt':'Estrelas:',            'en':'Stars:',              'es':'Estrellas:'},
    
    # ── MERCADO / HARAS ────────────────────────────────────────────────────────
    'seu_haras':             {'pt':'Seu Haras',            'en':'Your Stable',         'es':'Tu Haras'},
    'comprar_haras':         {'pt':'Comprar / Fazer Upgrade','en':'Buy / Upgrade',     'es':'Comprar / Mejorar'},
    'sem_baia':              {'pt':'Sem baias livres!','en':'No free stalls!','es':'Sin establos libres!'},
    'cavalos_mercado':       {'pt':'Cavalos no Mercado',   'en':'Horses on Market',    'es':'Caballos en el Mercado'},
    'cavalos_disponiveis':   {'pt':'Cavalos Disponiveis',  'en':'Available Horses',    'es':'Caballos Disponibles'},
    'filtrar':               {'pt':'Filtrar',              'en':'Filter',              'es':'Filtrar'},
    'velocidade_min':        {'pt':'Velocidade Minima:',   'en':'Min Speed:',          'es':'Velocidad Minima:'},
    'preco_max':             {'pt':'Preco Maximo:',        'en':'Max Price:',          'es':'Precio Maximo:'},
    'ordenar_por':           {'pt':'Ordenar por:',         'en':'Sort by:',            'es':'Ordenar por:'},
    'preco':                 {'pt':'Preco',                'en':'Price',               'es':'Precio'},
    
    # ── CRUZAMENTO ─────────────────────────────────────────────────────────────
    'cruzamento_titulo':     {'pt':'Cruzamento  R$800',    'en':'Breeding  R$800',     'es':'Cruza  R$800'},
    'cruzamento_desc':       {'pt':'Combine a genética de dois cavalos','en':'Combine genetics of two horses','es':'Combina la genetica de dos caballos'},
    'pai':                   {'pt':'Pai:',                 'en':'Sire:',               'es':'Padre:'},
    'mae':                   {'pt':'Mae:',                 'en':'Dam:',                'es':'Madre:'},
    'nome_filhote':          {'pt':'Nome do filhote:',     'en':'Foal name:',          'es':'Nombre del potro:'},
    'cor_filhote':           {'pt':'Cor do filhote:',      'en':'Foal color:',         'es':'Color del potro:'},
    'raca_filhote':          {'pt':'Raca do filhote:',     'en':'Foal breed:',         'es':'Raza del potro:'},
    'gerar_filhote':         {'pt':'Gerar Filhote (R$800)','en':'Breed Foal (R$800)',  'es':'Generar Potro (R$800)'},
    'vel_media':             {'pt':'Vel media:',           'en':'Avg Speed:',          'es':'Vel media:'},
    'previsao_filhote':      {'pt':'Previsao do Filhote:', 'en':'Foal Forecast:',      'es':'Prediccion del Potro:'},
    
    # ── GENEALOGIA ─────────────────────────────────────────────────────────────
    'genealogia_titulo':     {'pt':'Genealogia',           'en':'Genealogy',           'es':'Genealogia'},
    'arvore_familia':        {'pt':'Arvore Genealogica',   'en':'Family Tree',         'es':'Arbol Genealogico'},
    'linhagem':              {'pt':'Linhagem',             'en':'Lineage',             'es':'Linaje'},
    
    # ── PATROCINADORES ────────────────────────────────────────────────────────────
    'patrocinadores':        {'pt':'Patrocinadores Ativos','en':'Active Sponsors',    'es':'Patrocinadores Activos'},
    'disponivel':            {'pt':'Disponivel',           'en':'Available',           'es':'Disponible'},
    'condicao':              {'pt':'Condicao:',            'en':'Condition:',          'es':'Condicion:'},
    'pagamento':             {'pt':'Pagamento:',           'en':'Payment:',            'es':'Pago:'},
    'duracao':               {'pt':'Duracao:',             'en':'Duration:',           'es':'Duracion:'},
    'sem_patrocinador':      {'pt':'Nenhum patrocinador ativo.','en':'No active sponsors.','es':'Sin patrocinadores activos.'},
    
    # ── BANCO ──────────────────────────────────────────────────────────────────
    'seu_banco':             {'pt':'Seu Banco',            'en':'Your Bank',           'es':'Tu Banco'},
    'saldo':                 {'pt':'Saldo:',               'en':'Balance:',            'es':'Saldo:'},
    'emprestimos':           {'pt':'Emprestimos',          'en':'Loans',               'es':'Prestamos'},
    'contratar_emprestimo':  {'pt':'Contratar Emprestimo', 'en':'Take Loan',           'es':'Contratar Prestamo'},
    'parcela_semanal':       {'pt':'Parcela Semanal:',     'en':'Weekly Installment:', 'es':'Cuota Semanal:'},
    'juros':                 {'pt':'Juros:',               'en':'Interest:',           'es':'Interes:'},
    'sem_emprestimo':        {'pt':'Nenhum emprestimo ativo.','en':'No active loans.','es':'Sin prestamos activos.'},
    'semanal_de':            {'pt':'semanal de',           'en':'weekly for',          'es':'semanal durante'},
    'parcela':               {'pt':'Parcela',              'en':'Installment',         'es':'Cuota'},
    
    # ── APOSTAS ────────────────────────────────────────────────────────────────
    'apostas_titulo':        {'pt':'Sistema de Apostas',   'en':'Betting System',      'es':'Sistema de Apuestas'},
    'proximo_cavalo':        {'pt':'Proximo Cavalo:',      'en':'Next Horse:',         'es':'Proximo Caballo:'},
    'valor_aposta':          {'pt':'Valor da Aposta:',     'en':'Bet Amount:',         'es':'Monto de Apuesta:'},
    'apostar':               {'pt':'Apostar',              'en':'Bet',                 'es':'Apostar'},
    'minimo_aposta':         {'pt':'Aposta minima: R$10',  'en':'Min bet: R$10',       'es':'Apuesta minima: R$10'},
    'aposta_confirmada':     {'pt':'Aposta Confirmada!',   'en':'Bet Confirmed!',      'es':'Apuesta Confirmada!'},
    
    # ── TROFÉUS ────────────────────────────────────────────────────────────────
    'trofeus_titulo':        {'pt':'Galeria de Trofeus',   'en':'Trophy Gallery',      'es':'Galeria de Trofeos'},
    'conquistas':            {'pt':'conquistas',           'en':'achievements',        'es':'logros'},
    'nenhuma_conquista':     {'pt':'Nenhuma conquista ainda.','en':'No achievements yet.','es':'Sin logros aun.'},
    'resumo_geral':          {'pt':'Resumo Geral',         'en':'Overall Summary',     'es':'Resumen General'},
    'trofeus_camp':          {'pt':'Trofeus de Campeonato','en':'Championship Trophies','es':'Trofeos de Campeonato'},
    'medalhas_corrida':      {'pt':'Medalhas de Corrida',  'en':'Race Medals',         'es':'Medallas de Carrera'},
    'primeiro':              {'pt':'1 Lugar',              'en':'1st Place',           'es':'1er Lugar'},
    'segundo':               {'pt':'2 Lugar',              'en':'2nd Place',           'es':'2do Lugar'},
    'terceiro':              {'pt':'3 Lugar',              'en':'3rd Place',           'es':'3er Lugar'},
    'ouro':                  {'pt':'Ouro',                 'en':'Gold',                'es':'Oro'},
    'prata':                 {'pt':'Prata',                'en':'Silver',              'es':'Plata'},
    'bronze':                {'pt':'Bronze',               'en':'Bronze',              'es':'Bronce'},
    'trofeu':                {'pt':'Trofeu',               'en':'Trophy',              'es':'Trofeo'},
    'total_vitorias':        {'pt':'Total de Vitorias:',   'en':'Total Wins:',         'es':'Total de Victorias:'},
    'streak_atual':          {'pt':'Streak Atual:',        'en':'Current Streak:',     'es':'Racha Actual:'},
    
    # ── RESULTADO ──────────────────────────────────────────────────────────────
    'vitoria':               {'pt':'VITORIA!',             'en':'VICTORY!',            'es':'VICTORIA!'},
    'lugar2':                {'pt':'2 Lugar!',             'en':'2nd Place!',          'es':'2do Lugar!'},
    'lugar3':                {'pt':'3 Lugar!',             'en':'3rd Place!',          'es':'3er Lugar!'},
    'fora_top3':             {'pt':'Fora do Top 3',        'en':'Outside Top 3',       'es':'Fuera del Top 3'},
    'premio':                {'pt':'Premio',               'en':'Prize',               'es':'Premio'},
    'aposta_resultado':      {'pt':'Aposta',               'en':'Bet',                 'es':'Apuesta'},
    'patrocinio_receb':      {'pt':'Patrocinio',           'en':'Sponsorship',         'es':'Patrocinio'},
    'parcela_cobrada':       {'pt':'Parcela',              'en':'Installment',         'es':'Cuota'},
    'manutencao_cobrada':    {'pt':'Manutencao',           'en':'Maintenance',         'es':'Mantenimiento'},
    'proxima_corrida':       {'pt':'Proxima Corrida',      'en':'Next Race',           'es':'Proxima Carrera'},
    'encerrar_camp':         {'pt':'Encerrar Campeonato',  'en':'End Championship',    'es':'Terminar Campeonato'},
    'ir_menu':               {'pt':'Menu',                 'en':'Menu',                'es':'Menu'},
    'resultado_corrida':     {'pt':'Resultado da Corrida', 'en':'Race Result',         'es':'Resultado de la Carrera'},
    
    # ── FUNCIONÁRIOS ───────────────────────────────────────────────────────────
    'funcionarios_titulo':   {'pt':'Funcionarios do Haras', 'en':'Stable Staff',       'es':'Personal del Haras'},
    'funcionarios_disponiveis': {'pt':'Funcionarios Disponiveis','en':'Available Staff','es':'Personal Disponible'},
    'contratar':             {'pt':'Contratar',            'en':'Hire',                'es':'Contratar'},
    'custo_semanal':         {'pt':'Custo Semanal:',       'en':'Weekly Cost:',        'es':'Costo Semanal:'},
    'demitir':               {'pt':'Demitir',              'en':'Fire',                'es':'Despedir'},
    'expertise':             {'pt':'Expertise:',           'en':'Expertise:',          'es':'Experiencia:'},
    
    # ── CALENDÁRIO ─────────────────────────────────────────────────────────────
    'calendario_titulo':     {'pt':'Calendario',           'en':'Calendar',            'es':'Calendario'},
    'proximo_evento':        {'pt':'Proximo Evento:',      'en':'Next Event:',         'es':'Proximo Evento:'},
    'evento_semanal':        {'pt':'Evento Semanal:',      'en':'Weekly Event:',       'es':'Evento Semanal:'},
    
    # ── LEILÃO ─────────────────────────────────────────────────────────────────
    'leilao_titulo':         {'pt':'Leilao de Cavalos',    'en':'Horse Auction',       'es':'Subasta de Caballos'},
    'leilao_ativo':          {'pt':'Leilao Ativo!',        'en':'Active Auction!',     'es':'Subasta Activa!'},
    'leilao_encerrado':      {'pt':'Leilao Encerrado',     'en':'Auction Closed',      'es':'Subasta Cerrada'},
    'proximo_leilao':        {'pt':'Proximo Leilao em:',   'en':'Next Auction in:',    'es':'Proxima Subasta en:'},
    'lance_atual':           {'pt':'Lance Atual:',         'en':'Current Bid:',        'es':'Oferta Actual:'},
    'dar_lance':             {'pt':'Dar Lance',            'en':'Place Bid',           'es':'Dar Oferta'},
    'ganho_lance':           {'pt':'GANHOU!',              'en':'WON!',                'es':'GANO!'},
    'perdeu_lance':          {'pt':'Superado por outro lance.','en':'Outbid.','es':'Superado por otra oferta.'},
    
    # ── CONFIGURAÇÕES ──────────────────────────────────────────────────────────
    'cfg_titulo':            {'pt':'Configuracoes',        'en':'Settings',            'es':'Configuracion'},
    'cfg_idioma':            {'pt':'Idioma / Language / Idioma','en':'Language / Idioma / Idioma','es':'Idioma / Language / Idioma'},
    'cfg_som':               {'pt':'Som',                  'en':'Sound',               'es':'Sonido'},
    'cfg_som_on':            {'pt':'Som: LIGADO',          'en':'Sound: ON',           'es':'Sonido: ACTIVO'},
    'cfg_som_off':           {'pt':'Som: DESLIGADO',       'en':'Sound: OFF',          'es':'Sonido: INACTIVO'},
    'cfg_lang_atual':        {'pt':'Idioma atual:',        'en':'Current language:',   'es':'Idioma actual:'},
    'cfg_aplicar':           {'pt':'Aplicar',              'en':'Apply',               'es':'Aplicar'},
    'cfg_salvo':             {'pt':'Configuracoes salvas!','en':'Settings saved!',     'es':'Configuracion guardada!'},
    'cfg_limpar_jogo':       {'pt':'Limpar Jogo (Restart)', 'en':'Clear Game (Restart)','es':'Limpiar Juego (Reiniciar)'},
    
    # ── LOGIN / SPLASH ─────────────────────────────────────────────────────────
    'novo_jogo':             {'pt':'Novo Jogo',            'en':'New Game',            'es':'Nuevo Juego'},
    'seu_nome':              {'pt':'Seu Nome:',            'en':'Your Name:',          'es':'Tu Nombre:'},
    'iniciar_jogo':          {'pt':'Iniciar Jogo',         'en':'Start Game',          'es':'Iniciar Juego'},
    'project_horse':         {'pt':'Project Horse',        'en':'Project Horse',       'es':'Project Horse'},
    'bem_vindo':             {'pt':'Bem-vindo!',           'en':'Welcome!',            'es':'Bienvenido!'},
    'carregar_save':         {'pt':'Carregando save...',   'en':'Loading save...',     'es':'Cargando guardado...'},
    
    # ── INFORMAÇÕES GERAIS ─────────────────────────────────────────────────────
    'semana_atual':          {'pt':'Semana atual:',        'en':'Current week:',       'es':'Semana actual:'},
    'dinheiro':              {'pt':'Dinheiro:',            'en':'Money:',              'es':'Dinero:'},
    'r_symbol':              {'pt':'R$',                   'en':'R$',                  'es':'R$'},
    'salvo_com_sucesso':     {'pt':'Jogo salvo com sucesso!','en':'Game saved!','es':'Juego guardado!'},
    'carregado_sucesso':     {'pt':'Jogo carregado!',      'en':'Game loaded!',        'es':'Juego cargado!'},
    'erro_salvar':           {'pt':'Erro ao salvar!',      'en':'Error saving!',       'es':'Error al guardar!'},
    'erro_carregar':         {'pt':'Erro ao carregar!',    'en':'Error loading!',      'es':'Error al cargar!'},
    
    # ── DIÁLOGOS E MENSAGENS ───────────────────────────────────────────────────
    'confirma_venda':        {'pt':'Tem certeza que deseja vender?','en':'Are you sure?','es':'Estás seguro?'},
    'confirma_deletar':      {'pt':'Tem certeza? Acao irreversivel!','en':'Sure? Irreversible!','es':'Seguro? Irreversible!'},
    'fundo_insuficiente':    {'pt':'Fundo insuficiente!',  'en':'Insufficient funds!', 'es':'Fondos insuficientes!'},
    'valor_minimo':          {'pt':'Valor minimo nao atingido!','en':'Min value not met!','es':'Valor minimo no alcanzado!'},
    'sucesso':               {'pt':'Sucesso!',             'en':'Success!',            'es':'Exito!'},
    'erro':                  {'pt':'Erro!',                'en':'Error!',              'es':'Error!'},
    'aviso':                 {'pt':'Aviso',                'en':'Warning',             'es':'Advertencia'},
    
    # ── COMPETIÇÕES ────────────────────────────────────────────────────────────
    'regional':              {'pt':'Regional',             'en':'Regional',            'es':'Regional'},
    'nacional':              {'pt':'Nacional',             'en':'National',            'es':'Nacional'},
    'internacional':         {'pt':'Internacional',        'en':'International',       'es':'Internacional'},
    
    # ── RAÇAS ──────────────────────────────────────────────────────────────────
    'puro_sangue':           {'pt':'Puro Sangue Inglês',   'en':'English Thoroughbred','es':'Pura Sangre Inglés'},
    'arabe':                 {'pt':'Árabe',                'en':'Arabian',             'es':'Árabe'},
    'turcomeno':             {'pt':'Turcomeno',            'en':'Turkmene',            'es':'Turcomano'},
    'quarto_milha':          {'pt':'Quarto de Milha',      'en':'Quarter Horse',       'es':'Cuarto de Milla'},
    'mustang':               {'pt':'Mustang',              'en':'Mustang',             'es':'Mustang'},
    'appaloosa':             {'pt':'Appaloosa',            'en':'Appaloosa',           'es':'Appaloosa'},
    'mestico':               {'pt':'Mestiço',              'en':'Mixed',               'es':'Mestizo'},
    # ── CHAVES ADICIONAIS ──────────────────────────────────────────────────────
    'manut_label':        {'pt':'Manut:',                 'en':'Maint:',                   'es':'Mant:'},
    'slogan':             {'pt':'Seu haras, seu campeonato','en':'Your stable, your championship','es':'Tu haras, tu campeonato'},
    'simulador':          {'pt':'Simulador de Haras',       'en':'Stable Simulator',         'es':'Simulador de Haras'},
    'hint_nome':          {'pt':'Nome do treinador...',     'en':'Trainer name...',          'es':'Nombre del entrenador...'},
    'hint_potro':         {'pt':'Ex: Trovao Jr',            'en':'E.g.: Thunder Jr',         'es':'Ej: Trueno Jr'},
    'emprestimos_ativos': {'pt':'Emprestimos ativos:',      'en':'Active loans:',            'es':'Prestamos activos:'},
    'solicitar_emprestimo':{'pt':'Solicitar emprestimo:',   'en':'Request loan:',            'es':'Solicitar prestamo:'},
    'contratos_assinados':{'pt':'Todos contratos assinados!','en':'All contracts signed!',   'es':'Todos los contratos firmados!'},
    'classif_atual':      {'pt':'Classificacao atual',      'en':'Current standings',        'es':'Clasificacion actual'},
    'classif_final':      {'pt':'Classificacao Final',      'en':'Final standings',          'es':'Clasificacion Final'},
    'premiacao_final':    {'pt':'Premiacao Final',          'en':'Final Prize',              'es':'Premiacion Final'},
    'premio_por_corrida': {'pt':'Premio por corrida:',      'en':'Prize per race:',          'es':'Premio por carrera:'},
    'premio_final':       {'pt':'Premio final:',            'en':'Final prize:',             'es':'Premio final:'},
    'nasceu':             {'pt':'Nasceu:',                  'en':'Born:',                    'es':'Nacio:'},
    'va_mercado':         {'pt':'Va ao Mercado e compre seu primeiro!','en':'Go to Market and buy your first!','es':'Ve al Mercado y compra tu primero!'},
    'gestacao':           {'pt':'Gestacao',                 'en':'Pregnancy',                'es':'Gestacion'},
    'nasce_semanas':      {'pt':'Nasce em 8 semanas',       'en':'Born in 8 weeks',          'es':'Nace en 8 semanas'},
    'compre_baia':        {'pt':'Compre uma baia na aba Baias.','en':'Buy a stall in the Stalls tab.','es':'Compra un establo en la pestana.'},
    'mercado_vazio':      {'pt':'Mercado vazio.',           'en':'Empty market.',            'es':'Mercado vacio.'},
    'para':               {'pt':'Para:',                    'en':'For:',                     'es':'Para:'},
    'selecionar':         {'pt':'Selecionar',               'en':'Select',                   'es':'Seleccionar'},
    'sem_leilao':         {'pt':'Sem leilao ativo no momento.','en':'No active auction right now.','es':'Sin subasta activa ahora.'},
    'leilao_desc':        {'pt':'Leiloes trazem cavalos 4 e 5 estrelas,','en':'Auctions bring 4 and 5 star horses,','es':'Las subastas traen caballos 4 y 5 estrellas,'},
    'proximo_lance':      {'pt':'Proximo lance:',           'en':'Next bid:',                'es':'Proxima oferta:'},
    'lance_max':          {'pt':'Lance maximo atingido',    'en':'Maximum bid reached',      'es':'Oferta maxima alcanzada'},
    'sem_cavalos':        {'pt':'Sem cavalos.',             'en':'No horses.',               'es':'Sin caballos.'},
    'trocar_animal':      {'pt':'Toque para trocar o animal:','en':'Tap to switch the horse:','es':'Toque para cambiar el animal:'},
    'nenhuma_conquista':  {'pt':'Nenhuma conquista ainda.', 'en':'No achievements yet.',     'es':'Sin logros aun.'},
    'venca_corridas':     {'pt':'Venca corridas e campeonatos!','en':'Win races and championships!','es':'Gana carreras y campeonatos!'},
    'medalhas':           {'pt':'Medalhas',                 'en':'Medals',                   'es':'Medallas'},
    'recordes_haras':     {'pt':'Recordes do Haras',        'en':'Stable Records',           'es':'Records del Haras'},
    'nenhuma_corrida':    {'pt':'Nenhuma corrida ainda.',   'en':'No races yet.',            'es':'Sin carreras aun.'},
    'voltar_menu_comp':   {'pt':'Volte ao menu para a proxima competicao!','en':'Go back to menu for next competition!','es':'Vuelve al menu para la proxima competicion!'},
    # ── TREINO ─────────────────────────────────────────────────────────────────
    'treinar_btn':           {'pt':'Treinar -100 Ouro',    'en':'Train -100 Gold',     'es':'Entrenar -100 Oro'},
    'treinar_titulo':        {'pt':'Treino de Cavalo',     'en':'Horse Training',      'es':'Entrenamiento'},
    'treinar_vel':           {'pt':'Velocidade melhorada!','en':'Speed improved!',     'es':'Velocidad mejorada!'},
    'treinar_ganho':         {'pt':'Vel. melhorada em',    'en':'Speed improved by',   'es':'Vel. mejorada en'},
    'treinar_energia':       {'pt':'Energia gasta: -20',   'en':'Energy spent: -20',   'es':'Energia gastada: -20'},
    'sem_ouro_treino':       {'pt':'Precisa de 100 Ouro para treinar!','en':'Need 100 Gold to train!','es':'Necesita 100 Oro para entrenar!'},
    'resultado_treino':      {'pt':'Resultado do Treino',  'en':'Training Result',     'es':'Resultado del Entrenamiento'},

    # ── TROFEUS / REPUTAÇÃO ─────────────────────────────────────────────────────
    'reputacao_haras':       {'pt':'Reputacao do Haras',   'en':'Stable Reputation',   'es':'Reputacion del Haras'},
    'reputacao_max':         {'pt':'Reputacao MAXIMA!',    'en':'MAX Reputation!',     'es':'Reputacion MAXIMA!'},
    'pts_totais':            {'pt':'pts totais',           'en':'total pts',           'es':'pts totales'},
    'pts_para':              {'pt':'pts para',             'en':'pts to reach',        'es':'pts para'},
    'nivel_iniciante':       {'pt':'Iniciante',            'en':'Beginner',            'es':'Principiante'},
    'nivel_conhecido':       {'pt':'Conhecido',            'en':'Known',               'es':'Conocido'},
    'nivel_respeitado':      {'pt':'Respeitado',           'en':'Respected',           'es':'Respetado'},
    'nivel_famoso':          {'pt':'Famoso',               'en':'Famous',              'es':'Famoso'},
    'nivel_lendario':        {'pt':'Lendario',             'en':'Legendary',           'es':'Legendario'},
    'bonus_rep':             {'pt':'+5 vitoria  +2 podio  +30 campeonato  +3 entrevista',
                              'en':'+5 win  +2 podium  +30 championship  +3 interview',
                              'es':'+5 victoria  +2 podio  +30 campeonato  +3 entrevista'},
    'conquistas':            {'pt':'Conquistas',           'en':'Achievements',        'es':'Logros'},
    'trofeus_titulo':        {'pt':'Galeria de Trofeus',   'en':'Trophy Gallery',      'es':'Galeria de Trofeos'},

    # ── PATROCINADORES ─────────────────────────────────────────────────────────
    'contratos_ativos':      {'pt':'Contratos Ativos',     'en':'Active Contracts',    'es':'Contratos Activos'},
    'pagando':               {'pt':'PAGANDO',              'en':'PAYING',              'es':'PAGANDO'},
    'sem_restantes':         {'pt':'sem restantes',        'en':'weeks left',          'es':'sem restantes'},
    'cond_topo':             {'pt':'Top',                  'en':'Top',                 'es':'Top'},
    'cond_seguidas':         {'pt':'por',                  'en':'for',                 'es':'por'},
    'cond_semanas':          {'pt':'semanas seguidas',     'en':'consecutive weeks',   'es':'semanas seguidas'},
    'pat_disponiveis':       {'pt':'Patrocinios disponiveis:','en':'Available sponsorships:','es':'Patrocinios disponibles:'},
    'pat_limite':            {'pt':'Limite atingido: 1 por temporada.','en':'Limit reached: 1 per season.','es':'Limite alcanzado: 1 por temporada.'},
    'ouro_por_sem':          {'pt':'Ouro/sem',             'en':'Gold/week',           'es':'Oro/sem'},
    'disponivel':            {'pt':'Disponiveis',          'en':'Available',           'es':'Disponibles'},
    'contratos_assinados':   {'pt':'Todos os contratos ja foram assinados!','en':'All contracts already signed!','es':'Todos los contratos ya firmados!'},

    # ── BANCO / EMPRÉSTIMO ─────────────────────────────────────────────────────
    'pegar_emprestimo':      {'pt':'Pegar',                'en':'Take',                'es':'Tomar'},
    'bloqueado':             {'pt':'Bloqueado',            'en':'Locked',              'es':'Bloqueado'},
    'amanha':                {'pt':'Amanha',               'en':'Tomorrow',            'es':'Manana'},
    'ver_ad':                {'pt':'Ver Ad',               'en':'Watch Ad',            'es':'Ver Anuncio'},
    'ad_gratis':             {'pt':'Ver Anuncio — Ganhe Ouro Gratis!','en':'Watch Ad — Get Free Gold!','es':'Ver Anuncio — Gana Oro Gratis!'},
    'ouro_por_anuncio':      {'pt':'+1.000 Ouro por anuncio','en':'+1,000 Gold per ad','es':'+1.000 Oro por anuncio'},
    'divida_label':          {'pt':'Divida total:',        'en':'Total debt:',         'es':'Deuda total:'},

    # ── CORRIDA ─────────────────────────────────────────────────────────────────
    'escolha_cavalo':        {'pt':'Escolha o cavalo:',    'en':'Choose your horse:',  'es':'Elige tu caballo:'},
    'semana_label':          {'pt':'Semana',               'en':'Week',                'es':'Semana'},
    'ouro_label':            {'pt':'Ouro',                 'en':'Gold',                'es':'Oro'},
    'saldo_label':           {'pt':'Saldo: Ouro',          'en':'Balance: Gold',       'es':'Saldo: Oro'},
    'cavalos_risco':         {'pt':'Cavalos em risco',     'en':'Horses at risk',      'es':'Caballos en riesgo'},
    'substituto':            {'pt':'Considere cruzar ou comprar um substituto!',
                              'en':'Consider breeding or buying a replacement!',
                              'es':'Considera cruzar o comprar un sustituto!'},
    'sem_dividas':           {'pt':'Sem dividas!',         'en':'Debt free!',          'es':'Sin deudas!'},

    # ── RECORDES ─────────────────────────────────────────────────────────────────
    'rec_ricos':             {'pt':'Haras Mais Ricos — Patrimonio Total','en':'Richest Stables — Total Assets','es':'Haras Mas Ricos — Patrimonio Total'},
    'rec_plantel':           {'pt':'Maior Plantel — Qtd. de Cavalos','en':'Largest Roster — No. of Horses','es':'Mayor Plantel — Cant. de Caballos'},
    'rec_valiosos':          {'pt':'Cavalos Mais Valiosos','en':'Most Valuable Horses', 'es':'Caballos Mas Valiosos'},
    'rec_vitorias':          {'pt':'Mais Vitorias Globais','en':'Most Global Wins',     'es':'Mas Victorias Globales'},
    'rec_resumo':            {'pt':'Seu Haras — Resumo',   'en':'Your Stable — Summary','es':'Tu Haras — Resumen'},
    'patrimonio':            {'pt':'Patrimonio',           'en':'Assets',               'es':'Patrimonio'},
    'sua_posicao':           {'pt':'Sua posicao:',         'en':'Your position:',       'es':'Tu posicion:'},

    # ── FUNCIONÁRIOS ────────────────────────────────────────────────────────────
    'contratar':             {'pt':'Contratar',            'en':'Hire',                'es':'Contratar'},
    'demitir':               {'pt':'Demitir',              'en':'Fire',                'es':'Despedir'},
    'salario_sem':           {'pt':'Ouro/sem',             'en':'Gold/week',           'es':'Oro/sem'},

    # ── LEILÃO ──────────────────────────────────────────────────────────────────
    'leilao_titulo':         {'pt':'Leilao de Cavalos',    'en':'Horse Auction',       'es':'Subasta de Caballos'},
    'lendario_badge':        {'pt':'LENDARIO',             'en':'LEGENDARY',           'es':'LEGENDARIO'},
    'dar_lance':             {'pt':'DAR LANCE',            'en':'PLACE BID',           'es':'PUJAR'},
    'arrematado':            {'pt':'ARREMATADO',           'en':'SOLD',                'es':'REMATADO'},
    'proximo_leilao':        {'pt':'Proximo leilao em',    'en':'Next auction in',     'es':'Proxima subasta en'},

    # ── CONFIG ────────────────────────────────────────────────────────────────
    'config_titulo':         {'pt':'Configuracoes',        'en':'Settings',            'es':'Configuracion'},
    'som_on':                {'pt':'Som ON',               'en':'Sound ON',            'es':'Sonido ON'},
    'som_off':               {'pt':'Som OFF',              'en':'Sound OFF',           'es':'Sonido OFF'},
    'idioma':                {'pt':'Idioma',               'en':'Language',            'es':'Idioma'},
    'politica':              {'pt':'Politica de Privacidade','en':'Privacy Policy',    'es':'Politica de Privacidad'},

    # ── APOSTAS ────────────────────────────────────────────────────────────────
    'apostar_btn':           {'pt':'Apostar',              'en':'Bet',                 'es':'Apostar'},
    'valor_ouro':            {'pt':'Valor em Ouro...',     'en':'Amount in Gold...',   'es':'Monto en Oro...'},
    'minhas_apostas':        {'pt':'Minhas Apostas',       'en':'My Bets',             'es':'Mis Apuestas'},
    'apostas_titulo':        {'pt':'Apostas',              'en':'Bets',                'es':'Apuestas'},

    # ── HARAS / GERAL ────────────────────────────────────────────────────────
    'haras_label':           {'pt':'Haras',                'en':'Stable',              'es':'Haras'},
    'estrelas_label':        {'pt':'estrela(s)',           'en':'star(s)',             'es':'estrella(s)'},
    'ir_menu':               {'pt':'Menu Principal',       'en':'Main Menu',           'es':'Menu Principal'},
    'novo_jogo':             {'pt':'Novo Jogo',            'en':'New Game',            'es':'Nuevo Juego'},
    'hint_nome':             {'pt':'Nome do seu haras...',  'en':'Your stable name...', 'es':'Nombre de tu haras...'},
    'va_mercado':            {'pt':'Va ao Mercado e compre seu primeiro!','en':'Go to Market and buy your first!','es':'Ve al Mercado y compra tu primero!'},

    # ── STRINGS RESTANTES ────────────────────────────────────────────────────
    'sem_label':             {'pt':'Sem',                  'en':'Week',                'es':'Sem'},
    'haras_nome':            {'pt':'Haras',                'en':'Stable',              'es':'Haras'},
    'divida_total':          {'pt':'Dívida total:',        'en':'Total debt:',         'es':'Deuda total:'},
    'emprestimo_ativo':      {'pt':'Você já possui um empréstimo ativo.','en':'You already have an active loan.','es':'Ya tienes un prestamo activo.'},
    'quite_atual':           {'pt':'Quite o empréstimo atual antes de solicitar outro.','en':'Pay off the current loan before requesting another.','es':'Paga el prestamo actual antes de solicitar otro.'},
    'juros_label':           {'pt':'juros',                'en':'interest',            'es':'intereses'},
    'parcelas_label':        {'pt':'10x',                  'en':'10x',                 'es':'10x'},
    'ver_anuncio_gratis':    {'pt':'Ver Anuncio — Ganhe Ouro Gratis!','en':'Watch Ad — Get Free Gold!','es':'Ver Anuncio — Obtén Oro Gratis!'},
    'ouro_por_ad':           {'pt':'+1.000 Ouro por anuncio','en':'+1,000 Gold per ad','es':'+1.000 Oro por anuncio'},
    'evento_semana':         {'pt':'Evento da Semana',     'en':'Event of the Week',   'es':'Evento de la Semana'},
    'aposta_atual':          {'pt':'Aposta:',              'en':'Bet:',                'es':'Apuesta:'},
    'pts_corrida':           {'pt':'pts nesta corrida',    'en':'pts this race',       'es':'pts en esta carrera'},
    'potro_emergencia':      {'pt':'POTRO DE EMERGÊNCIA!', 'en':'EMERGENCY FOAL!',     'es':'POTRO DE EMERGENCIA!'},
    'doou_cavalo':           {'pt':'Um fazendeiro vizinho doou',   'en':'A neighboring farmer donated','es':'Un granjero vecino donó'},
    'ao_seu_haras':          {'pt':'ao seu haras!',        'en':'to your stable!',     'es':'a tu haras!'},
    'cuide_bem':             {'pt':'Cuide bem dele para reconstruir o haras.','en':'Take good care of it to rebuild the stable.','es':'Cuídalo bien para reconstruir el haras.'},
    'cavalos_risco':         {'pt':'Cavalos em risco',     'en':'Horses at risk',      'es':'Caballos en riesgo'},
    'saldo_ouro':            {'pt':'Saldo: Ouro',          'en':'Balance: Gold',       'es':'Saldo: Oro'},
    'baias_label':           {'pt':'Baias:',               'en':'Stalls:',             'es':'Establos:'},
    'vender_btn':            {'pt':'Vender',               'en':'Sell',                'es':'Vender'},
    'energia_btn':           {'pt':'Energia',              'en':'Energy',              'es':'Energía'},
    'treinar_btn2':          {'pt':'Treinar -100 Ouro',    'en':'Train -100 Gold',     'es':'Entrenar -100 Oro'},
    'sem_ouro_titulo':       {'pt':'Sem Ouro',             'en':'No Gold',             'es':'Sin Oro'},
    'resultado_treino':      {'pt':'Resultado do Treino',  'en':'Training Result',     'es':'Resultado del Entrenamiento'},
    'sem_baias':             {'pt':'Sem baias livres!',    'en':'No free stalls!',     'es':'Sin establos libres!'},
    'sem_cavalo_primeiro':   {'pt':'Compre um cavalo primeiro!','en':'Buy a horse first!','es':'Compra un caballo primero!'},
    'item_ouro':             {'pt':'Ouro',                 'en':'Gold',                'es':'Oro'},
    'leilao_titulo2':        {'pt':'Leilão de Cavalos',    'en':'Horse Auction',       'es':'Subasta de Caballos'},
    'leilao_lendarios':      {'pt':'incluindo cavalos LENDARIOS raros!','en':'including rare LEGENDARY horses!','es':'incluyendo caballos LEGENDARIOS raros!'},
    'gestacao_btn':          {'pt':'Iniciar Gestação (800 Ouro)','en':'Start Breeding (800 Gold)','es':'Iniciar Gestación (800 Oro)'},
    'gazeta':                {'pt':'GAZETA DO HARAS',      'en':'STABLE GAZETTE',      'es':'GACETA DEL HARAS'},
    'valor_aposta_hint':     {'pt':'Valor em Ouro...',     'en':'Amount in Gold...',   'es':'Monto en Oro...'},
    'salario_sem':           {'pt':'Ouro/sem',             'en':'Gold/week',           'es':'Oro/sem'},
    'contratar_btn':         {'pt':'Contratar',            'en':'Hire',                'es':'Contratar'},
    'sua_posicao_rank':      {'pt':'Sua posição:',         'en':'Your rank:',          'es':'Tu posición:'},
    'resumo_haras':          {'pt':'Seu Haras — Resumo',   'en':'Your Stable — Summary','es':'Tu Haras — Resumen'},
    'patrimonio_rank':       {'pt':'Patrimônio',           'en':'Assets',              'es':'Patrimonio'},
    'cavalo_mais_caro':      {'pt':'Cavalo mais caro:',    'en':'Most valuable horse:','es':'Caballo más caro:'},
    'haras_nivel_sem':       {'pt':'Haras nível',          'en':'Stable level',        'es':'Haras nivel'},
    'no_ranking':            {'pt':'no ranking',           'en':'in ranking',          'es':'en ranking'},
    'vitorias_totais':       {'pt':'Vitórias totais:',     'en':'Total wins:',         'es':'Victorias totales:'},
    'potro_raca':            {'pt':'Potro:',               'en':'Foal:',               'es':'Potro:'},
    'vel_aprox':             {'pt':'Vel ~',                'en':'Spd ~',               'es':'Vel ~'},

    # ── Resumo financeiro / Balanço ─────────────────────────────────────────
    'balanco_label':         {'pt':'Balanço',              'en':'Balance',             'es':'Balance'},
    'resultado_liquido':     {'pt':'Resultado líquido:',   'en':'Net result:',         'es':'Resultado neto:'},
    'leilao_aberto_notif':   {'pt':'LEILÃO ABERTO! Veja cavalos raros!','en':'AUCTION OPEN! See rare horses!','es':'¡SUBASTA ABIERTA! ¡Caballos raros!'},
    'receitas_label':        {'pt':'Receitas',             'en':'Income',              'es':'Ingresos'},
    'despesas_label':        {'pt':'Despesas',             'en':'Expenses',            'es':'Gastos'},
    'premio_corrida_label':  {'pt':'Prêmio corrida',       'en':'Race prize',          'es':'Premio carrera'},
    'aposta_label':          {'pt':'Aposta',               'en':'Bet',                 'es':'Apuesta'},
    'manutencao_label':      {'pt':'Manutenção cavalos',   'en':'Horse maintenance',   'es':'Mantenimiento'},
    'func_label':            {'pt':'Funcionários',         'en':'Staff',               'es':'Empleados'},
    'parcela_emp_label':     {'pt':'Parcela empréstimo',   'en':'Loan installment',    'es':'Cuota préstamo'},
    'nenhuma_receita':       {'pt':'Nenhuma receita',      'en':'No income',           'es':'Sin ingresos'},
    # ── Config (chaves que faltavam) ─────────────────────────────────────────
    'cfg_titulo':            {'pt':'Configurações',        'en':'Settings',            'es':'Configuración'},
    'cfg_som':               {'pt':'Som',                  'en':'Sound',               'es':'Sonido'},
    'cfg_som_on':            {'pt':'Som ON',               'en':'Sound ON',            'es':'Sonido ON'},
    'cfg_som_off':           {'pt':'Som OFF',              'en':'Sound OFF',           'es':'Sonido OFF'},
    'cfg_idioma':            {'pt':'Idioma',               'en':'Language',            'es':'Idioma'},
    'req_reputacao':         {'pt':'Reputação necessária:','en':'Reputation required:','es':'Reputación requerida:'},
    'rep_estrelas_min':      {'pt':'★ mínimo para',       'en':'★ minimum for',       'es':'★ mínimo para'},

}


def set_lang(codigo: str):
    """Define o idioma ativo. Aceita 'pt', 'en', 'es'."""
    global _LANG
    if codigo in ('pt','en','es'):
        _LANG = codigo
        print(f'[I18N] Idioma alterado para: {codigo.upper()}')


def get_lang() -> str:
    return _LANG


def T(chave: str, **kwargs) -> str:
    """Retorna a tradução da chave no idioma atual.
    Aceita kwargs para str.format(**kwargs).
    """
    row = _TR.get(chave)
    if not row:
        print(f'[I18N] Chave não encontrada: {chave}')
        return chave
    txt = row.get(_LANG, row.get('pt', chave))
    if kwargs:
        try:
            txt = txt.format(**kwargs)
        except Exception as e:
            print(f'[I18N] Erro ao formatar: {chave} - {e}')
    return txt
