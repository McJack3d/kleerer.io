// SPDX-License-Identifier: CC-BY-NC-SA-4.0
// Copyright (C) 2026 kleerer. Licence: ../LICENSE-DATA.md
//
// kleerer. — evidence dataset. What the trials actually show, by need.
//
// EVERY NUMBER HERE POINTS AT A SOURCE. If a figure has no citation it does not
// go in. Grades are for the OUTCOME on this row, not for the supplement — the
// same molecule can be A for one thing and D for another, and usually is.
//
// The EFSA line is deliberately separate from the trial evidence. An EFSA
// authorised claim (Reg. 1924/2006) is regulator-approved WORDING about a
// nutrient's physiological role; it is not a trial showing an outcome improved.
// "Magnesium contributes to normal psychological function" is an authorised
// claim; "magnesium improves your sleep" has low-certainty evidence. Both facts
// are shown, side by side, so nobody has to confuse them.
const t = (en, fr) => ({ en, fr });

const EVIDENCE = {
  version: "1.0", updated: "2026-09-06",

  grades: {
    A: { label: t("strong", "solide"),
         def: t("Several large randomised trials or meta-analyses totalling more than ~1,000 participants, a consistent direction, and an effect large enough to notice.",
                "Plusieurs grands essais randomisés ou méta-analyses totalisant plus de ~1 000 participants, une direction cohérente et un effet assez grand pour être perceptible.") },
    B: { label: t("moderate", "modérée"),
         def: t("Meta-analyses of smaller trials, or a few hundred to ~1,000 participants; consistent but modest — or strong only in a defined group, such as people who are deficient.",
                "Méta-analyses d'essais plus petits, ou quelques centaines à ~1 000 participants ; effet cohérent mais modeste — ou solide seulement dans un groupe défini, comme les personnes carencées.") },
    C: { label: t("limited", "limitée"),
         def: t("Few or small trials, low-certainty grading, inconsistent results, or a high risk of bias — including trials funded by the ingredient's manufacturer.",
                "Essais peu nombreux ou petits, certitude faible, résultats inconstants ou risque de biais élevé — y compris des essais financés par le fabricant de l'ingrédient.") },
    D: { label: t("not supported", "non étayée"),
         def: t("Null in large trials for this outcome, or only observational or animal data. Not the same as harmful — it means the claim has been tested and did not hold up.",
                "Résultat nul dans de grands essais pour ce critère, ou seulement des données observationnelles ou animales. Pas synonyme de nocif : la promesse a été testée et n'a pas tenu.") },
  },

  // The supplement registry. `cat` links to a comparator category; `kind`
  // decides the colour — botanicals are not nutrients and are shown apart.
  supplements: {
    melatonin:    { name: t("melatonin", "mélatonine"),          cat: "melatonin",    kind: "nutrient" },
    magnesium:    { name: t("magnesium", "magnésium"),           cat: "magnesium",    kind: "nutrient" },
    creatine:     { name: t("creatine", "créatine"),             cat: "creatine",     kind: "nutrient" },
    whey:         { name: t("whey / protein", "whey / protéines"), cat: "whey",       kind: "nutrient" },
    vitamin_d3:   { name: t("vitamin D3", "vitamine D3"),        cat: "vitamin_d3",   kind: "nutrient" },
    omega3:       { name: t("omega-3 (EPA/DHA)", "oméga-3 (EPA/DHA)"), cat: "omega3", kind: "nutrient" },
    vitamin_c:    { name: t("vitamin C", "vitamine C"),          cat: "vitamin_c",    kind: "nutrient" },
    zinc:         { name: t("zinc", "zinc"),                     cat: "zinc",         kind: "nutrient" },
    probiotics:   { name: t("probiotics", "probiotiques"),       cat: "probiotics",   kind: "nutrient" },
    collagen:     { name: t("collagen peptides", "peptides de collagène"), cat: "collagen", kind: "nutrient" },
    multivitamin: { name: t("multivitamin", "multivitamines"),   cat: "multivitamin", kind: "nutrient" },
    ashwagandha:  { name: t("ashwagandha", "ashwagandha"),       cat: "ashwagandha",  kind: "botanical" },
    maca:         { name: t("maca", "maca"),                     cat: "maca",         kind: "botanical" },
    rhodiola:     { name: t("rhodiola", "rhodiola"),             cat: "rhodiola",     kind: "botanical" },
    curcumin:     { name: t("curcumin (turmeric)", "curcumine (curcuma)"), cat: "curcumin", kind: "botanical" },
  },

  needs: [
  // ------------------------------------------------------------------ sleep
  { id: "sleep", name: t("sleep", "sommeil"),
    blurb: t("The most-searched need and the one with the widest gap between what is sold and what is shown. Effects here are measured in minutes, not hours.",
             "Le besoin le plus recherché, et celui où l'écart est le plus grand entre ce qui se vend et ce qui se démontre. Les effets se mesurent ici en minutes, pas en heures."),
    entries: [
      { sup: "melatonin", grade: "B",
        effect: t("Falls asleep about 7 minutes sooner; sleeps about 8 minutes longer. Real, consistent, and small. Best evidence is for sleep onset and jet lag; in adults with plain insomnia the newer analysis found no significant effect.",
                  "Endormissement environ 7 minutes plus tôt ; sommeil environ 8 minutes plus long. Réel, cohérent et petit. Les meilleures preuves concernent l'endormissement et le décalage horaire ; chez l'adulte souffrant d'insomnie simple, l'analyse la plus récente ne trouve pas d'effet significatif."),
        dose: t("0.5–1.9 mg, 30–60 min before bed. 1.9 mg is the French ceiling for supplements.", "0,5–1,9 mg, 30–60 min avant le coucher. 1,9 mg est le plafond français pour les compléments."),
        studies: [
          { ref: "Ferracioli-Oda et al., PLoS One 2013", n: 1683, design: t("meta-analysis, 19 RCTs", "méta-analyse, 19 ECR"),
            finding: t("sleep onset −7.1 min (95% CI 4.4–9.8); total sleep +8.3 min", "endormissement −7,1 min (IC 95 % 4,4–9,8) ; sommeil total +8,3 min"),
            url: "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0063773" },
          { ref: "Sleep Medicine Reviews 2022", n: null, design: t("systematic review, 24 RCTs in chronic insomnia", "revue systématique, 24 ECR dans l'insomnie chronique"),
            finding: t("significant in children and adolescents; in adults with non-comorbid insomnia, not significant for onset, total sleep or efficiency", "significatif chez l'enfant et l'adolescent ; chez l'adulte sans comorbidité, non significatif sur l'endormissement, la durée ou l'efficacité"),
            url: "https://pubmed.ncbi.nlm.nih.gov/36179487/" },
        ],
        efsa: t("Authorised: \"contributes to the reduction of time taken to fall asleep\" (1 mg before bed) and \"alleviation of subjective feelings of jet lag\" (0.5 mg).",
                "Autorisée : « contribue à réduire le temps d'endormissement » (1 mg avant le coucher) et « atténuation des effets du décalage horaire » (0,5 mg)."),
        caveats: t("Timing matters more than dose. Longer trials and higher doses showed larger effects, but the whole effect is still under ten minutes.", "Le moment de la prise compte plus que la dose. Les essais plus longs et les doses plus élevées montrent des effets plus grands, mais l'effet total reste inférieur à dix minutes.") },

      { sup: "magnesium", grade: "C",
        effect: t("The popular claim, and the evidence does not carry it. Three small trials in older adults found sleep onset ~17 minutes sooner, at low-to-very-low certainty; a 2025 review of all adult trials concluded it should not be a routine insomnia treatment.",
                  "La promesse populaire, et les preuves ne la portent pas. Trois petits essais chez des adultes âgés trouvent un endormissement ~17 minutes plus tôt, avec une certitude faible à très faible ; une revue 2025 de tous les essais adultes conclut qu'il ne doit pas être un traitement de routine de l'insomnie."),
        dose: t("Trials used 320–500 mg/day elemental Mg. EFSA supplemental limit: 250 mg/day.", "Les essais ont utilisé 320–500 mg/j de Mg élémentaire. Limite EFSA pour les compléments : 250 mg/j."),
        studies: [
          { ref: "Mah & Pitre, BMC Complement Med Ther 2021", n: 151, design: t("meta-analysis, 3 RCTs, older adults", "méta-analyse, 3 ECR, adultes âgés"),
            finding: t("sleep onset −17.4 min; total sleep +16 min not significant; all trials moderate-to-high risk of bias", "endormissement −17,4 min ; sommeil total +16 min non significatif ; tous les essais à risque de biais modéré à élevé"),
            url: "https://link.springer.com/article/10.1186/s12906-021-03297-z" },
          { ref: "Systematic review of adult RCTs, 2025", n: null, design: t("systematic review", "revue systématique"),
            finding: t("certainty low to very low; modest benefit on some subjective outcomes, inconsistent; not supported as routine treatment", "certitude faible à très faible ; bénéfice modeste sur certains critères subjectifs, inconstant ; non étayé comme traitement de routine"),
            url: "https://pubmed.ncbi.nlm.nih.gov/42661485/" },
        ],
        efsa: t("No authorised sleep claim. Authorised: normal psychological function, reduction of tiredness and fatigue, normal muscle and nervous-system function.",
                "Aucune allégation sommeil autorisée. Autorisées : fonctions psychologiques normales, réduction de la fatigue, fonctions musculaire et nerveuse normales."),
        caveats: t("If you are actually low in magnesium — common with low intake, alcohol, some diuretics — correcting it can plausibly help. That is not the same as magnesium being a sleep aid for everyone.",
                   "Si vous manquez réellement de magnésium — fréquent avec un faible apport, l'alcool, certains diurétiques — corriger la carence peut aider. Ce n'est pas la même chose qu'un somnifère pour tout le monde.") },

      { sup: "ashwagandha", grade: "C",
        effect: t("A small-to-moderate improvement in sleep scores, strongest in people diagnosed with insomnia, at ≥600 mg/day for ≥8 weeks. Five small trials, mostly from Indian sites with links to extract manufacturers.",
                  "Amélioration petite à modérée des scores de sommeil, la plus nette chez les personnes diagnostiquées insomniaques, à ≥600 mg/j pendant ≥8 semaines. Cinq petits essais, surtout de sites indiens liés aux fabricants d'extraits."),
        dose: t("300–600 mg/day standardised root extract.", "300–600 mg/j d'extrait de racine standardisé."),
        studies: [
          { ref: "Cheah et al., PLoS One 2021", n: 400, design: t("meta-analysis, 5 RCTs", "méta-analyse, 5 ECR"),
            finding: t("overall sleep SMD −0.59 (−0.75 to −0.42), I² 62%; larger in insomnia, ≥600 mg, ≥8 weeks", "sommeil global DMS −0,59 (−0,75 à −0,42), I² 62 % ; plus marqué dans l'insomnie, ≥600 mg, ≥8 semaines"),
            url: "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0257843" },
        ],
        efsa: null,
        safety: "ashwagandha",
        caveats: t("Read the safety note before the dose.", "Lisez la note de sécurité avant la dose.") },
    ] },

  // --------------------------------------------------------- stress & anxiety
  { id: "stress", name: t("stress & anxiety", "stress & anxiété"),
    blurb: t("Where botanicals have their best evidence — and their loudest safety warnings.", "Là où les plantes ont leurs meilleures preuves — et leurs avertissements de sécurité les plus forts."),
    entries: [
      { sup: "ashwagandha", grade: "B",
        effect: t("Consistent reductions in perceived stress, anxiety scores and morning cortisol across a dozen trials. Effect sizes are moderate. Trials are short (30–90 days), mostly Indian, and often supported by the extract's manufacturer.",
                  "Réductions cohérentes du stress perçu, des scores d'anxiété et du cortisol matinal dans une douzaine d'essais. Effets modérés. Essais courts (30–90 jours), surtout indiens, souvent soutenus par le fabricant de l'extrait."),
        dose: t("300–600 mg/day standardised root extract (KSM-66, Sensoril, Shoden are the studied ones).", "300–600 mg/j d'extrait de racine standardisé (KSM-66, Sensoril, Shoden sont ceux étudiés)."),
        studies: [
          { ref: "Akhgarjand et al., Phytotherapy Research 2022", n: 1002, design: t("meta-analysis, 12 RCTs", "méta-analyse, 12 ECR"),
            finding: t("significant reduction in anxiety and stress scores", "réduction significative des scores d'anxiété et de stress"),
            url: "https://pubmed.ncbi.nlm.nih.gov/36017529/" },
          { ref: "Systematic review & meta-analysis, 2024", n: 558, design: t("meta-analysis, 9 RCTs", "méta-analyse, 9 ECR"),
            finding: t("perceived stress −4.7 points, anxiety −2.2, serum cortisol reduced; 125–600 mg/day for 30–90 days", "stress perçu −4,7 points, anxiété −2,2, cortisol sérique réduit ; 125–600 mg/j pendant 30–90 jours"),
            url: "https://pubmed.ncbi.nlm.nih.gov/39348746/" },
        ],
        efsa: t("None. Botanical claims are on hold under Reg. 1924/2006 — no ashwagandha claim is authorised.", "Aucune. Les allégations sur les plantes sont en attente sous le règlement 1924/2006 — aucune allégation ashwagandha n'est autorisée."),
        safety: "ashwagandha",
        caveats: t("The best-evidenced botanical on this page is also the one two European agencies have moved against. Both things are true.", "La plante la mieux étayée de cette page est aussi celle contre laquelle deux agences européennes ont agi. Les deux sont vrais.") },

      { sup: "magnesium", grade: "C",
        effect: t("Suggestive but poor-quality evidence for subjective anxiety. The authorised EFSA claim on \"psychological function\" describes a nutrient's role, not an anxiolytic effect.",
                  "Preuves suggestives mais de mauvaise qualité sur l'anxiété subjective. L'allégation EFSA autorisée sur les « fonctions psychologiques » décrit le rôle d'un nutriment, pas un effet anxiolytique."),
        dose: t("Trials: 75–360 mg/day.", "Essais : 75–360 mg/j."),
        studies: [
          { ref: "Boyle, Lawton & Dye, Nutrients 2017", n: null, design: t("systematic review, 18 studies", "revue systématique, 18 études"),
            finding: t("\"suggestive of a beneficial effect… the quality of the existing evidence is poor\"", "« suggère un effet bénéfique… la qualité des preuves existantes est mauvaise »"),
            url: "https://www.mdpi.com/2072-6643/9/5/429" },
        ],
        efsa: t("Authorised: \"contributes to normal psychological function\".", "Autorisée : « contribue à des fonctions psychologiques normales »."),
        caveats: null },

      { sup: "rhodiola", grade: "C",
        effect: t("Eleven small trials on physical and mental fatigue and stress; several positive, but two used no validated fatigue measure and the review declined to draw a conclusion.",
                  "Onze petits essais sur la fatigue physique et mentale et le stress ; plusieurs positifs, mais deux n'utilisaient aucune mesure validée de la fatigue et la revue a refusé de conclure."),
        dose: t("200–600 mg/day extract standardised to ~3% rosavins / 1% salidroside.", "200–600 mg/j d'extrait standardisé à ~3 % rosavines / 1 % salidroside."),
        studies: [
          { ref: "Ishaque et al., BMC Complement Altern Med 2012", n: 446, design: t("systematic review, 11 trials", "revue systématique, 11 essais"),
            finding: t("contradictory results, methodological limitations; no definite conclusion", "résultats contradictoires, limites méthodologiques ; aucune conclusion définitive"),
            url: "https://link.springer.com/article/10.1186/1472-6882-12-70" },
        ],
        efsa: null,
        caveats: t("Products vary enormously in standardisation; a trial's extract and a shelf product may share a name and little else.", "Les produits varient énormément en standardisation ; l'extrait d'un essai et un produit en rayon peuvent partager un nom et pas grand-chose d'autre.") },
    ] },

  // -------------------------------------------------------- muscle & strength
  { id: "muscle", name: t("muscle & strength", "muscle & force"),
    blurb: t("The best-evidenced corner of the whole supplement market. Two things work, both only with training.", "Le coin le mieux étayé de tout le marché des compléments. Deux choses marchent, toutes deux uniquement avec l'entraînement."),
    entries: [
      { sup: "creatine", grade: "A",
        effect: t("Around 1.1–1.4 kg more lean mass and measurably more strength than training alone, replicated across dozens of trials in young and old. Monohydrate is the studied form; nothing else has earned a premium.",
                  "Environ 1,1–1,4 kg de masse maigre en plus et davantage de force que l'entraînement seul, répliqué dans des dizaines d'essais chez jeunes et âgés. Le monohydrate est la forme étudiée ; aucune autre n'a mérité de surcoût."),
        dose: t("3–5 g/day, every day, no loading needed.", "3–5 g/j, chaque jour, sans phase de charge."),
        studies: [
          { ref: "Chilibeck et al., Open Access J Sports Med 2017", n: 721, design: t("meta-analysis, 22 RCTs, older adults", "méta-analyse, 22 ECR, adultes âgés"),
            finding: t("+1.37 kg lean tissue mass vs placebo, plus greater chest- and leg-press strength", "+1,37 kg de masse maigre vs placebo, plus de force au développé couché et à la presse"),
            url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5679696" },
          { ref: "Kreider et al., ISSN position stand, JISSN 2017", n: null, design: t("position stand", "position officielle"),
            finding: t("creatine monohydrate is the most effective ergogenic supplement available for high-intensity exercise capacity and lean mass", "le monohydrate de créatine est le complément ergogène le plus efficace disponible pour la capacité en effort intense et la masse maigre"),
            url: "https://jissn.biomedcentral.com/articles/10.1186/s12970-017-0173-z" },
        ],
        efsa: t("Authorised: \"increases physical performance in successive bursts of short-term, high-intensity exercise\" (3 g/day).", "Autorisée : « augmente les performances physiques lors d'efforts répétés de haute intensité et de courte durée » (3 g/j)."),
        caveats: t("Cognition is an emerging use — small trials, promising, not yet at the level of the muscle evidence.", "La cognition est un usage émergent — petits essais, prometteurs, pas encore au niveau des preuves musculaires.") },

      { sup: "whey", grade: "A",
        effect: t("Adds about 2.5 kg to a one-rep max and 0.3 kg of fat-free mass on top of resistance training. Benefits flatten around 1.6 g/kg/day total protein and shrink with age.",
                  "Ajoute environ 2,5 kg à un maximum sur une répétition et 0,3 kg de masse maigre en plus de l'entraînement en résistance. Le bénéfice plafonne vers 1,6 g/kg/j de protéines totales et diminue avec l'âge."),
        dose: t("Enough to reach ~1.6 g/kg/day total; ~20–40 g per serving.", "De quoi atteindre ~1,6 g/kg/j au total ; ~20–40 g par prise."),
        studies: [
          { ref: "Morton et al., Br J Sports Med 2018", n: 1863, design: t("meta-analysis & meta-regression, 49 RCTs", "méta-analyse et méta-régression, 49 ECR"),
            finding: t("1RM +2.49 kg, fat-free mass +0.30 kg; plateau ~1.6 g/kg/day; effect reduced with age", "1RM +2,49 kg, masse maigre +0,30 kg ; plateau ~1,6 g/kg/j ; effet réduit avec l'âge"),
            url: "https://pubmed.ncbi.nlm.nih.gov/28698222/" },
        ],
        efsa: t("Authorised: \"protein contributes to growth and maintenance of muscle mass\".", "Autorisée : « les protéines contribuent au développement et au maintien de la masse musculaire »."),
        caveats: t("It is protein that works, not whey specifically. Whey is a convenient, complete, fast source — food gets you the same place.", "C'est la protéine qui agit, pas la whey en particulier. La whey est une source pratique, complète et rapide — l'alimentation mène au même endroit.") },
    ] },

  // -------------------------------------------------------------------- bone
  { id: "bone", name: t("bone", "os"),
    blurb: t("The vitamin D story is the clearest example of \"deficiency correction works, blanket supplementation does not\".", "L'histoire de la vitamine D est l'exemple le plus clair de « corriger une carence marche, supplémenter tout le monde non »."),
    entries: [
      { sup: "vitamin_d3", grade: "D",
        effect: t("In 25,871 generally healthy adults not selected for deficiency, 2,000 IU/day for five years did not reduce fractures — total, hip or otherwise. For people who are actually deficient, correcting it remains standard care.",
                  "Chez 25 871 adultes globalement en bonne santé non sélectionnés pour carence, 2 000 UI/j pendant cinq ans n'ont pas réduit les fractures — totales, de hanche ou autres. Chez les personnes réellement carencées, corriger la carence reste la règle."),
        dose: t("800–2,000 IU/day if low; 4,000 IU is the EFSA upper limit. Test before you dose.", "800–2 000 UI/j si taux bas ; 4 000 UI est la limite supérieure EFSA. Dosez avant de supplémenter."),
        studies: [
          { ref: "LeBoff et al., NEJM 2022 (VITAL)", n: 25871, design: t("RCT, 5.3 years median", "ECR, 5,3 ans en médiane"),
            finding: t("no lower risk of total, non-vertebral or hip fractures vs placebo", "pas de risque réduit de fractures totales, non vertébrales ou de hanche vs placebo"),
            url: "https://www.nejm.org/doi/full/10.1056/NEJMoa2202106" },
        ],
        efsa: t("Authorised: normal bones and teeth, normal calcium absorption, normal muscle function, normal immune function.", "Autorisées : ossature et dents normales, absorption normale du calcium, fonction musculaire normale, fonction immunitaire normale."),
        caveats: t("The grade is for fracture prevention in the general population. Deficiency itself is common in France in winter, and its correction is a different — well-supported — question.", "La note porte sur la prévention des fractures en population générale. La carence est fréquente en France l'hiver, et sa correction est une autre question — bien étayée.") },
    ] },

  // ------------------------------------------------------------ heart & lipids
  { id: "heart", name: t("heart & blood pressure", "cœur & tension"),
    blurb: t("Prescription-dose EPA did something; supplement-dose fish oil, in the largest trial ever run, did not.", "L'EPA à dose pharmaceutique a fait quelque chose ; l'huile de poisson à dose complément, dans le plus grand essai jamais mené, non."),
    entries: [
      { sup: "omega3", grade: "C",
        effect: t("Triglyceride lowering is robust and dose-dependent — that part is settled. Cardiovascular events are not: 4 g/day of purified EPA cut events by 25% in high-risk patients (REDUCE-IT), while EPA+DHA at similar doses (STRENGTH) and 1 g/day fish oil in the general population (VITAL) did nothing. Shelf products are VITAL-dose products.",
                  "La baisse des triglycérides est robuste et dose-dépendante — ce point est tranché. Les événements cardiovasculaires non : 4 g/j d'EPA purifié ont réduit les événements de 25 % chez des patients à haut risque (REDUCE-IT), tandis qu'EPA+DHA à dose similaire (STRENGTH) et 1 g/j d'huile de poisson en population générale (VITAL) n'ont rien fait. Les produits en rayon sont des produits à dose VITAL."),
        dose: t("250 mg/day EPA+DHA meets the EFSA heart claim; 2 g/day for the triglyceride claim.", "250 mg/j d'EPA+DHA satisfont l'allégation cœur EFSA ; 2 g/j pour l'allégation triglycérides."),
        studies: [
          { ref: "Bhatt et al., NEJM 2019 (REDUCE-IT)", n: 8179, design: t("RCT, icosapent ethyl 4 g/day, high-risk patients", "ECR, icosapent éthyl 4 g/j, patients à haut risque"),
            finding: t("major cardiovascular events −25% relative; mineral-oil placebo since debated", "événements cardiovasculaires majeurs −25 % en relatif ; placebo à l'huile minérale contesté depuis"),
            url: "https://www.nejm.org/doi/full/10.1056/NEJMoa1812792" },
          { ref: "Nicholls et al., JAMA 2020 (STRENGTH)", n: 13078, design: t("RCT, EPA+DHA carboxylic acid 4 g/day", "ECR, EPA+DHA acide carboxylique 4 g/j"),
            finding: t("no reduction in cardiovascular events; stopped for futility", "pas de réduction des événements cardiovasculaires ; arrêté pour futilité"),
            url: "https://jamanetwork.com/journals/jama/fullarticle/2773120" },
          { ref: "Manson et al., NEJM 2019 (VITAL)", n: 25871, design: t("RCT, 1 g/day fish oil, general population", "ECR, 1 g/j d'huile de poisson, population générale"),
            finding: t("no reduction in major cardiovascular events or cancer", "pas de réduction des événements cardiovasculaires majeurs ni du cancer"),
            url: "https://www.nejm.org/doi/full/10.1056/NEJMoa1811403" },
        ],
        efsa: t("Authorised: EPA+DHA \"contribute to the normal function of the heart\" (250 mg/day), \"maintenance of normal blood triglyceride levels\" (2 g/day), \"normal blood pressure\" (3 g/day).", "Autorisées : EPA+DHA « contribuent au fonctionnement normal du cœur » (250 mg/j), « maintien d'une triglycéridémie normale » (2 g/j), « pression artérielle normale » (3 g/j)."),
        caveats: t("The one positive trial used a pharmaceutical, not a supplement, and its placebo is still argued about. Buying fish oil for your heart is buying the VITAL result.", "Le seul essai positif utilisait un médicament, pas un complément, et son placebo est encore débattu. Acheter de l'huile de poisson pour son cœur, c'est acheter le résultat VITAL.") },

      { sup: "magnesium", grade: "C",
        effect: t("A real but small blood-pressure reduction — about 2 mmHg systolic — across 34 trials.", "Une baisse de tension réelle mais petite — environ 2 mmHg systolique — sur 34 essais."),
        dose: t("Trials: median ~370 mg/day for ~3 months.", "Essais : médiane ~370 mg/j pendant ~3 mois."),
        studies: [
          { ref: "Zhang et al., Hypertension 2016", n: 2028, design: t("meta-analysis, 34 RCTs", "méta-analyse, 34 ECR"),
            finding: t("systolic −2.0 mmHg, diastolic −1.8 mmHg", "systolique −2,0 mmHg, diastolique −1,8 mmHg"),
            url: "https://www.ahajournals.org/doi/10.1161/HYPERTENSIONAHA.116.07664" },
        ],
        efsa: t("Authorised: \"contributes to electrolyte balance\".", "Autorisée : « contribue à l'équilibre électrolytique »."),
        caveats: t("Two millimetres is real and is also less than a brisk walk.", "Deux millimètres, c'est réel, et c'est aussi moins qu'une marche rapide.") },

      { sup: "multivitamin", grade: "D",
        effect: t("Fourteen thousand physicians, eleven years, a daily multivitamin: no effect on major cardiovascular events at all.", "Quatorze mille médecins, onze ans, une multivitamine quotidienne : aucun effet sur les événements cardiovasculaires majeurs."),
        dose: null,
        studies: [
          { ref: "Sesso et al., JAMA 2012 (Physicians' Health Study II)", n: 14641, design: t("RCT, 11.2 years", "ECR, 11,2 ans"),
            finding: t("major cardiovascular events HR 1.01 (0.91–1.10)", "événements cardiovasculaires majeurs HR 1,01 (0,91–1,10)"),
            url: "https://jamanetwork.com/journals/jama/fullarticle/1389615" },
        ],
        efsa: null, caveats: null },
    ] },

  // ------------------------------------------------------ immunity & infections
  { id: "immunity", name: t("immunity & colds", "immunité & rhumes"),
    blurb: t("\"Supports immunity\" is an authorised phrase for several nutrients. Whether you get fewer or shorter colds is a separate, and mostly disappointing, question.", "« Soutient l'immunité » est une formule autorisée pour plusieurs nutriments. Avoir moins de rhumes, ou des rhumes plus courts, est une autre question — et surtout décevante."),
    entries: [
      { sup: "vitamin_d3", grade: "C",
        effect: t("The 2017 pooled analysis found ~12% fewer people with at least one respiratory infection, strongest in those who were deficient and dosed daily. The 2025 update with newer trials found the overall effect had shrunk to non-significance.",
                  "L'analyse poolée de 2017 trouvait ~12 % de personnes en moins avec au moins une infection respiratoire, surtout chez les carencés dosés quotidiennement. La mise à jour 2025 avec de nouveaux essais trouve un effet global rétréci jusqu'à la non-significativité."),
        dose: t("Daily 800–2,000 IU if low. Bolus doses showed no benefit.", "800–2 000 UI/j si taux bas. Les doses massives espacées n'ont montré aucun bénéfice."),
        studies: [
          { ref: "Martineau et al., BMJ 2017", n: 11321, design: t("individual-participant-data meta-analysis, 25 RCTs", "méta-analyse sur données individuelles, 25 ECR"),
            finding: t("odds of ≥1 acute respiratory infection −12%; NNT 33; greatest benefit in the deficient and with daily/weekly dosing", "risque d'au moins 1 infection respiratoire aiguë −12 % ; NNT 33 ; bénéfice maximal chez les carencés et en prise quotidienne/hebdomadaire"),
            url: "https://www.bmj.com/content/356/bmj.i6583" },
          { ref: "Jolliffe et al., Lancet Diabetes Endocrinol 2025", n: null, design: t("updated meta-analysis, stratified aggregate data", "méta-analyse actualisée, données agrégées stratifiées"),
            finding: t("overall protective effect no longer statistically significant", "effet protecteur global plus statistiquement significatif"),
            url: "https://www.thelancet.com/journals/landia/article/PIIS2213-8587(24)00348-6/fulltext" },
        ],
        efsa: t("Authorised: \"contributes to the normal function of the immune system\".", "Autorisée : « contribue au fonctionnement normal du système immunitaire »."),
        caveats: null },

      { sup: "vitamin_c", grade: "C",
        effect: t("Taking it every day does not stop you catching colds. It shortens them slightly — 8% in adults, 14% in children. Starting it once the cold has begun does nothing consistent.",
                  "En prendre chaque jour n'empêche pas d'attraper des rhumes. Cela les raccourcit légèrement — 8 % chez l'adulte, 14 % chez l'enfant. Commencer une fois le rhume déclaré ne fait rien de cohérent."),
        dose: t("≥200 mg/day, regularly. Above ~1 g/day, absorption falls and the EFSA limit is 1,000 mg supplemental.", "≥200 mg/j, régulièrement. Au-delà de ~1 g/j l'absorption chute, et la limite EFSA est de 1 000 mg en complément."),
        studies: [
          { ref: "Hemilä & Chalker, Cochrane 2013", n: 11306, design: t("Cochrane review, 29 trial comparisons", "revue Cochrane, 29 comparaisons"),
            finding: t("no effect on incidence in the general population; duration −8% adults, −14% children with regular use", "aucun effet sur l'incidence en population générale ; durée −8 % adultes, −14 % enfants en prise régulière"),
            url: "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD000980.pub4/full" },
        ],
        efsa: t("Authorised: normal immune function, reduction of tiredness and fatigue, normal collagen formation, increases iron absorption.", "Autorisées : fonction immunitaire normale, réduction de la fatigue, formation normale de collagène, augmente l'absorption du fer."),
        caveats: t("The exception in the Cochrane data: people under heavy physical stress (marathoners, soldiers in the cold) halved their cold incidence. Everyone else did not.", "L'exception dans les données Cochrane : les personnes sous stress physique intense (marathoniens, soldats au froid) ont divisé par deux l'incidence. Pas les autres.") },

      { sup: "zinc", grade: "C",
        effect: t("Lozenges at ≥75 mg/day, started within 24 hours, shortened colds by about a third in seven trials. The 2024 Cochrane review is more cautious: maybe two days shorter, low certainty, and more nausea and bad taste.",
                  "Les pastilles à ≥75 mg/j, commencées sous 24 h, ont raccourci les rhumes d'environ un tiers dans sept essais. La revue Cochrane 2024 est plus prudente : peut-être deux jours de moins, certitude faible, et plus de nausées et de mauvais goût."),
        dose: t("Lozenges only, for the duration of the cold. The 25 mg/day EFSA limit is for long-term intake — not for a 5-day lozenge course.", "Pastilles uniquement, le temps du rhume. La limite EFSA de 25 mg/j vaut pour la prise au long cours — pas pour 5 jours de pastilles."),
        studies: [
          { ref: "Hemilä, Open Forum Infect Dis 2017", n: null, design: t("individual-patient meta-analysis, 7 RCTs, zinc acetate/gluconate lozenges", "méta-analyse sur données individuelles, 7 ECR, pastilles d'acétate/gluconate de zinc"),
            finding: t("cold duration −33% (95% CI 21–45%) at >75 mg/day", "durée du rhume −33 % (IC 95 % 21–45 %) à >75 mg/j"),
            url: "https://academic.oup.com/ofid/article/4/2/ofx059/3098578" },
          { ref: "Nault et al., Cochrane 2024", n: null, design: t("Cochrane review", "revue Cochrane"),
            finding: t("may shorten colds by ~2 days; low-certainty; more adverse events", "raccourcit peut-être le rhume de ~2 jours ; certitude faible ; plus d'effets indésirables"),
            url: "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.cd014914.pub2/full" },
        ],
        efsa: t("Authorised: normal immune function, normal cognitive function, normal fertility and reproduction, maintenance of normal testosterone levels, normal skin, hair and nails.", "Autorisées : fonction immunitaire normale, fonction cognitive normale, fertilité et reproduction normales, maintien d'un taux normal de testostérone, peau, cheveux et ongles normaux."),
        caveats: t("A zinc capsule swallowed daily is a different product from a lozenge dissolved in the mouth, and only the lozenge has cold evidence.", "Une gélule de zinc avalée chaque jour est un autre produit qu'une pastille dissoute en bouche, et seule la pastille a des preuves sur le rhume.") },

      { sup: "probiotics", grade: "B",
        effect: t("For one specific thing — diarrhoea caused by antibiotics — the evidence is good: about a third fewer cases in adults, and in children the Cochrane review calls it moderate-certainty. For \"immunity\" in general, no.",
                  "Pour une chose précise — la diarrhée causée par les antibiotiques — les preuves sont bonnes : environ un tiers de cas en moins chez l'adulte, et chez l'enfant la revue Cochrane parle de certitude modérée. Pour « l'immunité » en général, non."),
        dose: t("Trials mostly used ≥5–10 billion CFU/day, started with the antibiotic. Strain matters.", "Les essais ont surtout utilisé ≥5–10 milliards d'UFC/j, commencés avec l'antibiotique. La souche compte."),
        studies: [
          { ref: "Goodman et al., BMJ Open 2021", n: null, design: t("meta-analysis, adults", "méta-analyse, adultes"),
            finding: t("antibiotic-associated diarrhoea risk −37% with co-administration", "risque de diarrhée associée aux antibiotiques −37 % en co-administration"),
            url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC8362734/" },
          { ref: "Guo et al., Cochrane 2019", n: 6352, design: t("Cochrane review, 33 studies, children", "revue Cochrane, 33 études, enfants"),
            finding: t("moderate-certainty evidence that probiotics reduce antibiotic-associated diarrhoea", "preuves de certitude modérée que les probiotiques réduisent la diarrhée associée aux antibiotiques"),
            url: "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD004827.pub5/full" },
        ],
        efsa: t("None. No probiotic health claim has been authorised in the EU; the word \"probiotic\" itself is treated as an implied claim in several member states.", "Aucune. Aucune allégation probiotique n'a été autorisée dans l'UE ; le mot « probiotique » lui-même est traité comme une allégation implicite dans plusieurs États membres."),
        caveats: null },
    ] },

  // ------------------------------------------------------------- mood & mind
  { id: "mind", name: t("memory & mood", "mémoire & humeur"),
    blurb: t("Thin ground. One genuinely large, well-run trial programme, and it is the one most people would not expect.", "Terrain mince. Un seul programme d'essais vraiment grand et bien mené, et c'est celui que peu de gens attendraient."),
    entries: [
      { sup: "multivitamin", grade: "C",
        effect: t("In COSMOS, two years of a daily multivitamin improved episodic memory in adults over 60 — a small effect, from a single trial programme, with the product supplied by its manufacturer. Interesting, not yet settled.",
                  "Dans COSMOS, deux ans de multivitamine quotidienne ont amélioré la mémoire épisodique chez des adultes de plus de 60 ans — petit effet, un seul programme d'essais, produit fourni par son fabricant. Intéressant, pas encore tranché."),
        dose: null,
        studies: [
          { ref: "Vyas et al., Am J Clin Nutr 2024 (COSMOS)", n: 21442, design: t("RCT; clinic subcohort 573 + meta-analysis of 3 COSMOS cognitive substudies", "ECR ; sous-cohorte clinique 573 + méta-analyse de 3 sous-études cognitives COSMOS"),
            finding: t("episodic memory significantly improved vs placebo over 2 years", "mémoire épisodique significativement améliorée vs placebo sur 2 ans"),
            url: "https://ajcn.nutrition.org/article/S0002-9165(23)66342-7/fulltext" },
        ],
        efsa: null,
        caveats: t("Note the contrast with the heart row: the same kind of product, a decade earlier, did nothing for cardiovascular events in 14,641 men.", "Notez le contraste avec la ligne cœur : le même type de produit, dix ans plus tôt, n'a rien fait sur les événements cardiovasculaires chez 14 641 hommes.") },

      { sup: "creatine", grade: "C",
        effect: t("Small trials suggest modest gains in memory and processing speed, more so in older adults and under sleep deprivation. Promising and early.", "De petits essais suggèrent des gains modestes de mémoire et de vitesse de traitement, surtout chez les adultes âgés et en privation de sommeil. Prometteur et précoce."),
        dose: t("3–5 g/day, same as for muscle.", "3–5 g/j, comme pour le muscle."),
        studies: [],
        efsa: null,
        caveats: t("No large trial yet. Listed because the direction is consistent and the cost of being wrong is a few grams of a very safe powder.", "Aucun grand essai encore. Listé parce que la direction est cohérente et que le coût d'une erreur est quelques grammes d'une poudre très sûre.") },
    ] },

  // ------------------------------------------------------------ joints & pain
  { id: "joints", name: t("joints & pain", "articulations & douleur"),
    blurb: t("Curcumin is the botanical with the best trial base for a specific complaint — and a specific safety history to go with it.", "La curcumine est la plante avec la meilleure base d'essais pour une plainte précise — et un historique de sécurité précis qui va avec."),
    entries: [
      { sup: "curcumin", grade: "B",
        effect: t("Across 23 trials in knee osteoarthritis, curcumin lowered pain and stiffness scores versus placebo. Trials are short (8–12 weeks), formulations differ wildly, and several are small or industry-linked.",
                  "Sur 23 essais dans l'arthrose du genou, la curcumine a réduit les scores de douleur et de raideur vs placebo. Essais courts (8–12 semaines), formulations très variables, plusieurs petits ou liés à l'industrie."),
        dose: t("Plain 95% extract: 1,000–1,500 mg curcuminoids/day. Enhanced-absorption forms (Meriva, BCM-95, Turmipure) use their own studied doses, usually 250–500 mg.", "Extrait simple à 95 % : 1 000–1 500 mg de curcuminoïdes/j. Les formes à absorption améliorée (Meriva, BCM-95, Turmipure) utilisent leurs propres doses étudiées, généralement 250–500 mg."),
        studies: [
          { ref: "Bayesian network meta-analysis, J Ethnopharmacology 2023", n: 2175, design: t("network meta-analysis, 23 studies, 7 countries", "méta-analyse en réseau, 23 études, 7 pays"),
            finding: t("VAS pain and total WOMAC significantly lower than placebo", "douleur EVA et WOMAC total significativement plus bas que le placebo"),
            url: "https://www.sciencedirect.com/science/article/pii/S0378874123013636" },
        ],
        efsa: null,
        safety: "curcumin",
        caveats: t("Raw turmeric powder is not the product the trials used. Absorption of plain curcumin is poor; every branded form exists to fix that, and each has its own — usually manufacturer-run — trial.", "La poudre de curcuma brute n'est pas le produit des essais. L'absorption de la curcumine simple est mauvaise ; chaque forme brevetée existe pour y remédier, avec son propre essai — généralement mené par le fabricant.") },

      { sup: "collagen", grade: "C",
        effect: t("A handful of small trials report less activity-related joint pain at 5–10 g/day. Mostly manufacturer-funded; the skin-row funding pattern applies here too.", "Une poignée de petits essais rapportent moins de douleurs articulaires liées à l'activité à 5–10 g/j. Surtout financés par les fabricants ; le schéma de financement de la ligne peau s'applique ici aussi."),
        dose: t("5–10 g/day hydrolysed peptides.", "5–10 g/j de peptides hydrolysés."),
        studies: [],
        efsa: null, caveats: null },
    ] },

  // -------------------------------------------------------------------- skin
  { id: "skin", name: t("skin", "peau"),
    blurb: t("A textbook case of why funding is a variable, not a footnote.", "Un cas d'école montrant pourquoi le financement est une variable, pas une note de bas de page."),
    entries: [
      { sup: "collagen", grade: "C",
        effect: t("Pooled, 26 trials say hydration and elasticity improve. Re-analysed by who paid: in trials without industry funding, and in the higher-quality trials, the effect disappears. Two meta-analyses, two years apart, and the second one changes the answer.",
                  "Poolés, 26 essais disent que l'hydratation et l'élasticité s'améliorent. Réanalysés selon qui a payé : dans les essais sans financement industriel, et dans les essais de meilleure qualité, l'effet disparaît. Deux méta-analyses à deux ans d'écart, et la seconde change la réponse."),
        dose: t("2.5–10 g/day in the trials.", "2,5–10 g/j dans les essais."),
        studies: [
          { ref: "Indian J Dermatol Venereol Leprol 2023", n: 1721, design: t("meta-analysis, 26 RCTs", "méta-analyse, 26 ECR"),
            finding: t("hydration and elasticity significantly improved vs placebo", "hydratation et élasticité significativement améliorées vs placebo"),
            url: "https://ijdvl.com/effects-of-collagen-based-supplements-on-skins-hydration-and-elasticity-a-systematic-review-and-meta-analysis/" },
          { ref: "Am J Med 2025", n: 1474, design: t("meta-analysis, 23 RCTs, stratified by funding and quality", "méta-analyse, 23 ECR, stratifiée par financement et qualité"),
            finding: t("overall benefit; NO effect in non-industry-funded trials; NO effect in high-quality trials", "bénéfice global ; AUCUN effet dans les essais sans financement industriel ; AUCUN effet dans les essais de haute qualité"),
            url: "https://www.amjmed.com/article/S0002-9343(25)00283-9/abstract" },
        ],
        efsa: t("None authorised for collagen. Vitamin C carries \"normal collagen formation for the normal function of skin\".", "Aucune autorisée pour le collagène. La vitamine C porte « formation normale de collagène pour la fonction normale de la peau »."),
        caveats: null },
    ] },

  // --------------------------------------------------------------------- gut
  { id: "gut", name: t("gut", "intestin"),
    blurb: t("Probiotics are the rare category where \"it depends on the strain\" is a literal finding, not a hedge.", "Les probiotiques sont la rare catégorie où « ça dépend de la souche » est un résultat littéral, pas une esquive."),
    entries: [
      { sup: "probiotics", grade: "C",
        effect: t("For IBS, 53 trials show a modest improvement in global symptoms, with heterogeneity above 90% — meaning the average hides strains that work and strains that do not. See the immunity row for the one strong probiotic use.",
                  "Pour le SII, 53 essais montrent une amélioration modeste des symptômes globaux, avec une hétérogénéité au-delà de 90 % — l'average cache des souches qui marchent et d'autres non. Voir la ligne immunité pour le seul usage probiotique solide."),
        dose: t("Strain-specific; a product should name its strains with codes, not just species.", "Spécifique à la souche ; un produit doit nommer ses souches avec leurs codes, pas seulement l'espèce."),
        studies: [
          { ref: "Ford et al., Aliment Pharmacol Ther 2018", n: 5545, design: t("meta-analysis, 53 RCTs, IBS", "méta-analyse, 53 ECR, SII"),
            finding: t("modest benefit on global symptoms, pain and bloating; which strains is unclear", "bénéfice modeste sur les symptômes globaux, la douleur et le ballonnement ; quelles souches, on ne sait pas"),
            url: "https://pubmed.ncbi.nlm.nih.gov/30294792/" },
          { ref: "Network meta-analysis, 2024", n: 5531, design: t("network meta-analysis, 43 RCTs", "méta-analyse en réseau, 43 ECR"),
            finding: t("outcome-specific efficacy differs by strain and mixture; I² > 90%", "efficacité par critère différente selon souche et mélange ; I² > 90 %"),
            url: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10490209/" },
        ],
        efsa: null, caveats: null },
    ] },

  // ------------------------------------------------------------ energy & fatigue
  { id: "energy", name: t("energy & fatigue", "énergie & fatigue"),
    blurb: t("\"Reduces tiredness and fatigue\" is one of the most-printed authorised claims. It describes what a deficiency does, and if you are not deficient it describes nothing.", "« Réduit la fatigue » est l'une des allégations autorisées les plus imprimées. Elle décrit ce que fait une carence ; si vous n'êtes pas carencé, elle ne décrit rien."),
    entries: [
      { sup: "magnesium", grade: "C",
        effect: t("The claim is authorised; the trials in people who are not deficient are not there. The honest sentence is: if your intake is low, fixing it helps; if it is not, this is not an energy supplement.", "L'allégation est autorisée ; les essais chez les non-carencés n'existent pas. La phrase honnête : si votre apport est bas, le corriger aide ; sinon, ce n'est pas un complément énergie."),
        dose: null, studies: [],
        efsa: t("Authorised: \"contributes to a reduction of tiredness and fatigue\".", "Autorisée : « contribue à réduire la fatigue »."),
        caveats: t("The supplements that actually fix fatigue when a cause is found are iron and vitamin B12 — after a blood test, not before. Neither is a guessing-game purchase.", "Les compléments qui corrigent réellement la fatigue quand une cause est trouvée sont le fer et la vitamine B12 — après une prise de sang, pas avant. Aucun des deux ne s'achète à l'aveugle.") },

      { sup: "rhodiola", grade: "C",
        effect: t("See the stress row: 11 small trials, several positive, methodologically weak.", "Voir la ligne stress : 11 petits essais, plusieurs positifs, méthodologiquement faibles."),
        dose: t("200–600 mg/day standardised extract.", "200–600 mg/j d'extrait standardisé."),
        studies: [
          { ref: "Ishaque et al., BMC Complement Altern Med 2012", n: 446, design: t("systematic review, 11 trials", "revue systématique, 11 essais"),
            finding: t("3 of 5 mental-fatigue trials positive; two used no validated measure", "3 des 5 essais sur la fatigue mentale positifs ; deux sans mesure validée"),
            url: "https://link.springer.com/article/10.1186/1472-6882-12-70" },
        ],
        efsa: null, caveats: null },
    ] },

  // ---------------------------------------------------- sexual health & fertility
  { id: "sexual", name: t("libido & fertility", "libido & fertilité"),
    blurb: t("The category with the most confident marketing and the fewest participants.", "La catégorie au marketing le plus assuré et au plus petit nombre de participants."),
    entries: [
      { sup: "maca", grade: "C",
        effect: t("Four small trials in 2010, two in 2023 — that is the whole randomised evidence base. Some show more desire or better erectile scores; the reviews say the numbers are too small to conclude anything firm.",
                  "Quatre petits essais en 2010, deux en 2023 — c'est toute la base d'essais randomisés. Certains montrent plus de désir ou de meilleurs scores érectiles ; les revues disent que les effectifs sont trop petits pour conclure fermement."),
        dose: t("1.5–3 g/day powder in the trials, 6–12 weeks.", "1,5–3 g/j de poudre dans les essais, 6–12 semaines."),
        studies: [
          { ref: "Shin et al., BMC Complement Altern Med 2010", n: null, design: t("systematic review, 4 RCTs", "revue systématique, 4 ECR"),
            finding: t("limited evidence; number of trials, sample size and quality too limited for firm conclusions", "preuves limitées ; nombre d'essais, effectifs et qualité trop limités pour conclure"),
            url: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2928177/" },
          { ref: "J Men's Health 2023, erectile dysfunction", n: null, design: t("systematic review, 2 RCTs", "revue systématique, 2 ECR"),
            finding: t("limited evidence of benefit; more rigorous studies warranted", "preuves limitées de bénéfice ; des études plus rigoureuses sont nécessaires"),
            url: "https://www.jomh.org/articles/10.22514/jomh.2023.003" },
        ],
        efsa: null,
        caveats: t("Maca is safe and cheap, which is a reasonable basis for trying it and an unreasonable basis for the claims on the box.", "La maca est sûre et peu chère, ce qui est une base raisonnable pour essayer et une base déraisonnable pour les promesses de la boîte.") },

      { sup: "zinc", grade: "C",
        effect: t("Authorised claims on fertility and testosterone maintenance reflect zinc's role in deficiency. Supplementing replete men has not been shown to raise testosterone.", "Les allégations autorisées sur la fertilité et le maintien de la testostérone reflètent le rôle du zinc en cas de carence. Supplémenter des hommes non carencés n'a pas montré d'élévation de la testostérone."),
        dose: t("8–11 mg/day meets the reference intake; 25 mg/day is the EFSA limit.", "8–11 mg/j couvrent l'apport de référence ; 25 mg/j est la limite EFSA."),
        studies: [],
        efsa: t("Authorised: \"contributes to normal fertility and reproduction\", \"maintenance of normal testosterone levels in the blood\".", "Autorisées : « contribue à une fertilité et une reproduction normales », « maintien d'un taux normal de testostérone dans le sang »."),
        caveats: null },
    ] },
  ],

  // Safety notes referenced by `safety:` on an entry. Written to be shown
  // prominently, above the dose, because a reader who stops at the grade
  // should still have seen them.
  safety: {
    ashwagandha: {
      title: t("Two European agencies have moved against ashwagandha", "Deux agences européennes ont agi contre l'ashwagandha"),
      body: t("Denmark banned it in food and supplements in 2023, citing possible effects on thyroid and sex hormones and a possible abortifacient effect. In April 2024 ANSES (France) advised people with thyroid, liver or heart conditions or hyperandrogenism, pregnant or breastfeeding women, people on sedatives, and anyone under 18 not to take it. Case reports of liver injury exist, including one requiring transplant, and an EU food-safety working group has recommended a formal Article 8 safety review. kleerer does not red-card it — Denmark and ANSES are not among the three bodies in the red-card rule — but this is the strongest safety signal of any product on the site.",
               "Le Danemark l'a interdit dans les aliments et compléments en 2023, citant de possibles effets sur la thyroïde et les hormones sexuelles et un possible effet abortif. En avril 2024, l'ANSES a déconseillé sa consommation aux personnes atteintes de pathologies thyroïdiennes, hépatiques ou cardiaques ou d'hyperandrogénie, aux femmes enceintes ou allaitantes, aux personnes sous sédatifs et aux moins de 18 ans. Des cas d'atteinte hépatique existent, dont un ayant nécessité une greffe, et un groupe de travail européen a recommandé une procédure formelle de l'article 8. kleerer ne lui met pas de carton rouge — le Danemark et l'ANSES ne font pas partie des trois instances de la règle — mais c'est le signal de sécurité le plus fort de tout le site."),
      urls: [
        { label: "ANSES, avis 2021-SA-0077 du 19 avril 2024 (PDF)", url: "https://www.anses.fr/fr/system/files/NUT2021SA0077.pdf" },
        { label: "Regulatory roundup — Denmark, ANSES, EU Article 8", url: "https://www.nutritioninsight.com/news/regulatory-update-spotlight-on-international-authorities-response-to-ashwagandha-safety-concerns.html" },
        { label: "NIH ODS fact sheet", url: "https://ods.od.nih.gov/factsheets/Ashwagandha-HealthProfessional/" },
        { label: "Lancet Gastroenterol Hepatol 2024 — herbal hepatotoxicity", url: "https://www.thelancet.com/journals/langas/article/PIIS2468-1253(24)00324-8/fulltext" },
      ] },
    curcumin: {
      title: t("High-absorption curcumin and the liver", "Curcumine à haute absorption et foie"),
      body: t("In 2019 the Italian Ministry of Health issued a warning after a cluster of hepatitis cases linked to curcuma supplements, and case reports have continued with enhanced-bioavailability formulations. Plain turmeric in food carries no such signal. Anyone with liver disease, or on medication metabolised by the liver, should treat concentrated curcumin as a drug, not a spice.",
               "En 2019, le ministère italien de la Santé a émis un avertissement après une série de cas d'hépatite liés à des compléments de curcuma, et des cas continuent d'être rapportés avec les formulations à biodisponibilité améliorée. Le curcuma alimentaire ne porte aucun signal de ce type. Toute personne atteinte d'une maladie hépatique, ou sous médicament métabolisé par le foie, doit considérer la curcumine concentrée comme un médicament, pas une épice."),
      urls: [] },
  },
};
