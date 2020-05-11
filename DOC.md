# Introducció

En aquest document es presentaran els diferents algoritmes i metodologies que s'han utilitzat durant la pràctica, juntament amb l'anàlisis d'aquests i la seva implementació.
La documentació està estructurada en diferents apartats,preprocessament, alineament de seqüències i classificació, cada un explicant la seva funcionalitat.

# Main

Aquesta serà la funció principal del programa i tindrà com a objectiu la recollida d'arguments i la execució de la funcionalitat principal.

Els arguments acceptats són el següents:

+ -c "fitxer" : introdueix la localització del fitxer .csv que conté les mostres de les dades

# Preprocessament

En el preprocessament es recullen i classifiquen les dades obtingudes del fitxer .csv i els fitxers FASTA descarregats.

## Tractament de les seqüències del fitxer csv

### Pseudocodi

    function preprocess(csvpath):
        country_dictionary <- {}
        csvfile <- open file csvpath
        for row in csvfile:
            if all necessary data is not empty:
                values_tuples <- (get Accession,Release_Date and Length data)
                Geo_location <- get Country of row
                country_dictionary[Geo_Location] <- add values_tuples

        close file csvfile  
        medians_list <- []
        for country in all countries:
            sort country_dictionary[country] by Length data
            median_sample <- get country data located at the length based median location
            medians_list <- add median sample data
        return medians_list

### Cost teòric

Cost O(n(m+k)), on

+ n = number of lines in csv file,
+ m = number of keys in country_dictionay
+ k = length of string

## Obtenció del país de longitud mediana

Per tal d'obtenir un cost O(n) en l'obtenció de la mediana, ens hem basat en l'algoritme median of medians. Aquest algoritme divideix la llista original en diferents subllistes i calcula la mediana aproximada d'aquestes subllistes.
Un cop tenim aquestes medianes, es calcularà la mediana d'aquesta nova llista, la qual s'utilitzarà com a pivot. Seguidament es col·locaran els elements més petits o iguals al pivot a l'esquerra i els més grans a la dreta. Aquest procés es repetirà recursivament fins que la posició sigui exactament igual al número d'elements més petits que el pívot.

### Pseudocodi

    function get_median(country samples list, position) is
        sublist <- divide country samples list in sublists of 5 samples
        medians <- list of sublists medians
        if number of medians <= 5:
            pivot <- median of medians
        else:
            pivot <- recursive get_median(medians, median of medians)

        low <- elements lower or equal than pivot
        remove last element from low
        high <- elements higher than pivot

        k <- number of elements of low
        if position < k:
            return recursive get_median(low, position)
        elif position > k:
            return recursive get_median(high, position-k-1)
        else:
            return pivot

### Cost teòric

Cost O(n), on n és el nombre d'elements d'un país

## Obtenció de seqüències Fasta

### Pseudocodi

    function get_fasta_sequences(sample_list):
        for sample in sample_list:
            obtain fasta sequence of sample via HTTP
            if not response:
                ask user if continue or not
            split data by new line
            all subsequences of fasta sequence
            assign fasta sequence to sample

### Cost teòric

El cost teòric és d'ordre O(n(m+k)) tal que

+ n és el numero de mostres que hi ha a sample_list.
+ m és el temps d'obtenció de la seqüencia via HTTP.
+ k és numero de subseqüències que formen la seqüencia fasta.

# Alineament de seqüències

En l'alineament de seqüències es puntua la similitud entre dues seqüències. En el nostre cas, com més gran és aquest nombre, més similar és.

## Anàlisis dels algorismes existents

Pel que fa a l'alineament de seqüències s'han trobat els següents algorismes:

1. Algorisme de Needleman-Wunsch
    + Aquest algorisme utilitza programació dinàmica per a buscar un alineament "global" entre dues seqüències.
    Aquest algorisme utilitza ordre O(nm), ja que crea una matriu per a emmagatzemar les puntuacions dels diferents possibles alineaments a efectuar, i en finalitzar trobarà l'alineament òptim.
2. Algorisme de Smith-Waterman
    + Aquest algorisme utilitza una versió similar al de Needleman-Wunsch però aquest té com a objectiu buscar un alineament "local" entre dues seqüències.
    De totes maneres l'ordre serà de O(nm) per la mateixa raó que el mètode de Needleman-Wunsch, l'única diferència serà en el moment d'efectuar l'alineació un cop es té la matriu de les puntuacions parcials, on es començarà el procés des d'una posició diferent.
3. Algorisme de Hirschberg
    + Aquest algorisme també és una modificació basada en l'algorisme de Needleman-Wunsch, encara que manté l'ordre d'O(nm), millora la utilització de l'espai per part de les matrius.

En el nostre cas s'ha elegit l'algorisme de Needleman-Wunsch per les següents raons:

1. El cost teòric era el mateix en tots els algorismes utilitzats i per tant, pel que fa a aquesta característica la diferenciació entre els algorismes era irrellevant.

2. Encara que és cert alguns dels algorismes proporcionats tenen menor temps d'execució, al ser una diferència bastant petita, s'ha considerat innecessari preocupar-se'n.

3. La simplicitat d'efectuar l'algorisme també ha sigut una raó molt important en la seva selecció.

### Pseudocodi de l'algorisme seleccionat

Primerament s'ha de mencionar que l'algorisme s'inicia amb una matriu amb els costs de totes les transformacions possibles amb les dades de la seqüència:

Per exemple: A -> G = -3, A -> T = -8, etc

A més a més també s'ha d'afegir una penalització de gap.

Un cop fet es crearà una matriu amb les respostes parcials de la següent manera:

    int F[Longitud A][Longitud B]

    for i in range(0,Longitud A):
        F[i][0]=i*penalització de gap

    for j in range(0,Longitud B):
        F[0][j]=j*penalització de gap

    for i in range(1,Longitud A):
        for j in range(1,Longitud B):
            int Opcio1=F[i-1][j-1]+Cost transformació entre les lletres.
            int Opcio2=F[i-1][j]+penalització de gap
            int Opcio3=F[i][j-1]+penalització de gap
        F[i][j]=max(Opcio1,Opcio2,Opcio3)

Un cop tenim la matriu, la puntuació de similitud de la millor alineació serà la puntuació que es troba en la posició F[longitudA][longitudB].

També existeix una segona part de l'algorisme que tindria com a objectiu crear dos strings assenyalant com quedarien els strings un cop efectuada l'alineació òptima.  Com que en el nostre cas únicament volem saber la puntuació de l'alineament, aquesta segona part no l'hem efectuat.

### Anàlisis Teòric

Per a la implementació s'ha trobat el següent problema:

Com que les mostres a comprovar eren molt grans (29000 aprox.), el temps per a executar l'algorisme en Python era inacceptable.

Per a solucionar-lo s'havien proposat les següents accions:

1. Reduir la mida de la mostra a comprovar i únicament alinear els primers 1000 caràcters.

2. Intentar efectuar l'algorisme millorant Python amb llenguatges més ràpids com serien Rust, Haskell, C, C++, etc.

En el nostre cas s'ha decidit efectuar les dues mesures, el qual ha millorat enormement el temps d'execució.

Com hem dit anteriorment, el cost teòric serà O(nm), on

+ n = llargada seqüència 1
+ m = llargada seqüència 2

### Anàlisis Experimental
