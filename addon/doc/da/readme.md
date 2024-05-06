# Indrykningsnavigation #

* Forfatter: Tony Malykh
* Download [stabil version][1]

Denne tilføjelse giver NVDA-brugere mulighed for at navigere efter
indrykningsniveau eller forskydning af linjer eller afsnit. I browsere gør
denne pakke det muligt hurtigt at finde afsnit med samme forskydning fra
skærmens venstre kant som f.eks. kommentarer på første niveau i et
hierarkisk træ med kommentarer. Desuden tillader det at springe mellem
linjerne på samme indrykningsniveau og hurtigt finde linjer med større eller
mindre indrykkningsniveau, når du redigerer kildekoden i diverse
programmeringssprog.

## Brug i browsere
Indrykningsnavigation kan bruges til at navigere ved forskydning fra
skærmens venstre kant. Du kan trykke NVDA+Alt+pil ned eller pil op for at
hoppe til næste eller forrige afsnit, der har samme forskydning. For
eksempel kan dette være nyttigt, når du gennemser hierarkiske træer med
kommentarer (f.eks. På reddit.com) for at springe mellem kommentarer på
første niveau og springe over alle kommentarer på højere niveauer.

Rent ud sagt, så kan tilføjelsespakken bruges i enhver applikation, så længe
NVDA ha angivet et Tree Interceptor-objekt.

Kommandoer:

* NVDA+Alt+Pil op eller pil ned: Gå til forrige eller næste afsnit med samme
  forskydning.
* NVDA+Alt+Venstre pil: Gå til forrige afsnit med mindre forskydning.
* NVDA+Alt+Højre pil: Gå til næste afsnit med større forskydning.

## Anvendelse i tekstredigeringsværktøjer
Indrykningsnavigation kan også være nyttig til redigering af kildekoden på
mange programmeringssprog. Sprog som Python kræver, at kildekoden er korrekt
indrykket, mens det på mange andre programmeringssprog stærkt anbefales. Med
Indrykningsnavigation kan du trykke på NVDA+Alt+Pil ned eller pil op for at
hoppe til næste eller forrige linje med samme indrykningsniveau. Du kan også
trykke på NVDA+Alt+Venstre pil for at hoppe til en overordnet linje, som er
en tidligere linje med lavere indrykningsniveau. I Python kan du nemt finde
den aktuelle funktionsdefinition eller class-definition. Du kan også trykke
på NVDA+Alt+Højre pil for at gå til det første underordnede objekt i den
aktuelle linje, der henholdsvis er næste linje med større indrykningsniveau.

Hvis din NVDA er indstillet til at angive linjeindrykning som toner, vil
IndentNav hurtigt afspille tonerne af alle de linjer, du har sprunget
over. Hvis ikke, vil NVDA kun afspille korte lyde for omtrent at angive
antallet af linjer, du har sprunget over.

Kommandoer:

* NVDA+Alt+Pil op eller Pil ned: Spring til forrige eller næste linje med
  samme indrykningsniveau inden for den aktuelle indstillingsblok.
* NVDA+Ctrl+Pil op eller ned: Gennemtving hop til forrige eller næste linje
  med samme indrykningsniveau. Denne kommando vil hoppe til andre
  indrykningsblokke (f.eks. Andre Python-funktioner), hvis det er
  nødvendigt.
* NVDA+Alt+Venstre pil: Gå til overordnede objekt - dette er tidligere linje
  med mindre indrykningsniveau.
* NVDA+Alt+Højre pil: Gå til første underordnede objekt - dette er næste
  linje med større indrykningsniveau inden for samme indrykningsblok.

## Udgivelseshistorik
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Tilføjede understøttelse for internationalisering.
  * Tilføjet GPL-overskrifter i kildefilerne.
  * Mindre rettelser.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Første version.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav
