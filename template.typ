#let distance = 12.9
#let distanceAR = 2*distance
#let days = ("DAYS",)
#let nb = days.len()
#let period = "du " + days.first() + " au " + days.last()
#let price_per_km = "PRICE_PER_KM"
#let price = nb*distanceAR*price_per_km
#let date = datetime.today()

#set document(author: "FULLNAME", title: "Demande de remboursement des frais de déplacement du domicile au lieu de travail à bicyclette")
#set page(margin: (y: 1cm))
#set text(font: "Roboto", size: 9pt)

#block(
  width: 100%,
  [
    #set align(center)
    #image("Ecam_Logo_blue.svg", width: 25%),
  ]
)

#v(-5mm)

#block(
  stroke: 0.5pt,
  inset: 10pt,
  width: 100%,
  [
    #set align(center)
    #set text(weight: 700)
    DEMANDE DE REMBOURSEMENT DES FRAIS DE DEPLACEMENT DU DOMICILE AU LIEU DE TRAVAIL EN TRANSPORT EN COMMUN ET/OU A BICYCLETTE
  ]
)

#block([
  #set text(weight: 700)
  ATTENTION : Il convient de joindre à cette demande la copie des titres de transport et/ou le relevé des trajets à bicyclette effectués
])

#block(
  stroke: 0.5pt,
  inset: 10pt,
  width: 100%,
  [
    Nom: LASTNAME#h(1fr)  Prenom: FIRSTNAME#h(1fr)
    
    Adresse : ADDRESS 
    
    Institut : ECAM
    
    Période concernée : #period
  ]
)

#block(
  stroke: 0.5pt,
  inset: (x: 10pt, y: 5pt),
  [DEPLACEMENTS EN TRANSPORT EN COMMUN]
)


Formule d'abonnement (biffer la mention inutile) :
#block(
  inset: (left: 1.5cm),
  [
    #strike[Carte STIB]
    
    #strike[Carte TEC ou DE LIJN]
    
    #strike[Carte-train hebdomadaire]
    
    #strike[Carte-train mensuelle]
    
    #strike[Railflex]
    
    #strike[Abonnement SNCB annuel]
    
    #strike[Autre : ticket avec réduction Famille Nombreuse]

    #block(
      stroke: 0.5pt,
      inset: 10pt,
      width: 100%,
      [
        #underline[Pour les temps partiels uniquement :]
        #block(
          inset: (left: 1.5cm),
          [
            Autre employeur éventuel :
            
            Localisation :
            
            % temps de travail chez cet employeur :
            
            Intervention de cet (ces) employeur(s) :
          ]
        )
      ]
    )
  ]
)
            
#block(
  stroke: 0.5pt,
  inset: (x: 10pt, y: 5pt),
  [DEPLACEMENTS A BICYCLETTE]
)

Nombre de trajets effectués : #nb #h(2fr) Distance domicile lieu de travail A/R en km : #distanceAR km #h(1fr)

Remboursement demandé : #calc.round(price, digits: 2) €

#line(length: 100%, stroke: 0.5pt)

#box([
  Date : #date.display("[day]/[month]/[year]")

  Signature :
  #box(
    baseline: 90%,
    [
      #image("signature.png", width: 4cm, )
    ]
  )
])
#h(1fr)
#box(
  baseline: 0%,
  [
    #image("Logotype_Haute-ecole.jpg", width: 2.2cm)
  ]
)

#block(
  inset: (x: 2cm),
  [
    #table(
      stroke: 0.5pt,
      columns: (1fr, 1fr),
      inset: 5pt,
      align: horizon,
      table.cell(colspan: 2)[
        #set align(center)
        #set text(weight: 700)
        Réservé à l’administration
      ],
      [Montant total à rembourser :], [],
      [Visa service compétent :], [],
      [Accord Direction :],[],
      [Date transmission à la compta :],[],
    )
  ]
)
#pagebreak()
#block(
  stroke: 0.5pt,
  inset: (x: 10pt, y: 5pt),
  [RELEVÉ DES TRAJETS]
)

#(days.join("\n"))
#pagebreak()
#set page(flipped: true)

#v(1fr)
#figure(
  image("map.png", width: 100%),
  caption: [Le trajet effectué à vélo/unicycle électrique],
)
#v(1fr)
