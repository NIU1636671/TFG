# CONTINGUT TFG

En aquest repositori del projecte titutal: **L'ADN dels èxits musicals: Anàlisi i Recomanació basada en patrons**, trobaràs:

- **Article**
- **Codis:** Conté el codi de les diferents fases del projecte: Extracció de característiques, Detecció de patrons, Sistema de recomanació
- **Gràfic Interactiu:** En el següent apartat s'explica com utilitzar aquest gràfic i les diferencies de cada visualització
- **Arxius.pkl:** Contenen l'extracció de característiques per a que l'usuari pugui fer probes amb els codis.
- **TFG_BD_1:** Metadades de les cançons de la BD.

# GRÀFIC INTERACTIU - MANUAL D'ÚS

## Descripció 
Aquest gràfic interactiu representa punts corresponents a fragments de cançons del rànquing Billboard, agrupats segons paràmetres de clustering. El gràfic ha estat creat amb la llibreria Plotly.

## Com utilitzar el gràfic?

### **1 - OBRIR EL FTIXER HTML**
El primer pas, és obrir el arxiu html amb el teu navegador preferit, si no s'obre directament, descarrega el fitxer i torna-ho a intentar.

### **2 - EXPLORAR ELS PUNTS DEL GRÀFIC**
- Cada punt representa un fragment d'una cançó classificada
- En passar el cursor per sobre, es mostrà informació com:
  
  - Títol de la cançó
  - Nom del fitxer d'àudio
  - Gènere musical
  - Clúster al qual pertany

### **3 - INTERACCIÓ AMB EL GRÀFIC**
- Pots fer zoom seleccionant la zona amb el cursor
- Pots desplaçar el gràfic arrossegant-lo
- Al control lliscant de sota el gràfic, pots provar a augmentar o disminuir el valor d'èpsilon.

### 4 - INTERPRETACIÓ DELS ELEMENTS
- **Color**: Indica el clúster
- **Forma**: Representa el gènere
    
