Pokud je požadováno přemístění nákladu z jednoho místa do druhého, vozík si materiál vyzvedne do 1 minuty.
  - AMB_TEMPORAL, nejasnosť času (nevieme odkedy sa + minúta má počítať)
  - AMB_STATEMENT, rôzne slová pre 1 význam (náklad a materiál)
  - AMB_STATEMENT, nevhodne použité slovo miesto (nie je konkrétne)

*Pre účel premiestnenia materiálu zo zdrojovej stanice do cieľovej stanice sa používa vozík. Od spracovania požiadavku si vozík vyzdvihne materiál do  jednej minúty.*

Pokud se to nestihne, materiálu se nastavuje prioritní vlastnost.
  -	AMB_STATEMENT, nejasnosť čo sa nestihne

*V prípade, že od spracovania požiadavku vozík nevyzdvihne materiál do jednej minúty, tak sa vytvorí prioritný požiadavka od ktorého sa pridelí materiálu prioritná vlastnosť.*

Každý prioritní materiál musí být vyzvednutý vozíkem do 1 minuty od nastavení prioritního požadavku.
  -	UNSPECIFIED_SUBJECT, nevhodne použité spojenie: prioritní materiál
  -	DANGLING_ELSE, nejasnosť, čo sa stane v opačnom prípade (materíál nebude vyzvednuty do 1 minúty)

*Od vytvorenia prioritnej požiadavky bude materiál s prioritnou vlastnosťou vyzdvihnutý vozíkom do jednej minúty. V prípade, že materiál s prioritnou vlastnosťou nebude vyzdvihnutý vozíkom do jednej minúty, prepne sa do výnimky.*

Pokud vozík nakládá prioritní materiál, přepíná se do režimu pouze-vykládka.
  -	UNSPECIFIED_SUBJECT, nevhodne použité spojenie: prioritní materiál
  -	DANGLING_ELSE, nejasnosť, čo sa stane v opačnom prípade (vozík nenakladá prioritní materiál)

*Pokiaľ sa vozík zaoberá materiálom s prioritnou vlastnosťou, prepne sa do režimu iba-výklad. V prípade, že sa nezaoberá materiálom s prioritnou vlastnosťou, tak sa vozík do režimu iba-výklad neprepne.*

V tomto režimu zůstává, dokud nevyloží všechen takový materiál.
  -	AMB_STATEMENT, nejasnosť spojenia takový materiál

*V režime iba-výklad vozík zotrvá, dokiaľ nevyloží všetok materiál s prioritnou vlastnosťou.*

Normálně vozík během své jízdy může nabírat a vykládat další materiály v jiných zastávkách. 
  -	AMB_STATEMENT, rôzne slová pre 1 význam (miesto, zastávka)
  -	AMB_STATEMENT, nevhodne použitá dvojica slov (nabírat a vykládat)
  -	AMB_STATEMENT, nevhodne použité slovo Normálně (nie je konkrétne)

*Počas naplánovanej trasy môže vozík nakladať a vykladať ďalší materiál v iných zastávkach.*

Na jednom místě může vozík akceptovat nebo vyložit jeden i více materiálů.
  -	AMB_STATEMENT, nevhodne použité slovo akceptovať (nejasné)
  -	AMB_STATEMENT, nevhodne použité spojenie: Na jednom místě (nejasné, na akom)
  -	AMB_STATEMENT, nevhodne použité slovo miesto (nie je konkrétne)

*Na zastávke, kde sa momentálne vozík nachádza môže vozík nakladať alebo vykladať aj viacero materiálov.*

Pořadí vyzvednutí materiálů nesouvisí s pořadím vytváření požadavků.
  -	AMB_STATEMENT, nevhodne použité spojenie vytváření požadavků

*Pri premiestnení materiálu nie je poradie nakladania materiálov závislé od poradia spracovania požiadaviek.*

Vozík neakceptuje materiál, pokud jsou všechny jeho sloty obsazené nebo by jeho převzetím byla překročena maximální nosnost.
  -	AMB_STATEMENT, nevhodne použité slovo neakceptuje a slovo převzetím

*V prípade, že má vozík všetky sloty obsadené alebo by po naložení materiálu prekročil maximálnu nosnosť, tak vozík nenakladá tento materiál.*
