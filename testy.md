<h1>Dokumentácia testov</h1>
V tomto dokumente sa nachádza popis tabuľky CEF grafu, identifikácia vstupných parametrov testu a identifikácia charakteristiky parametrov + definícia ich blokov.

<h2>Popis tabuľky CEG grafu</h2>

| **Názov**  | **Popis** | **[1]** | **[2]** | **[3]** | **[4]** | 
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1  | spracovanie (normálneho) požiadavku  | 0 | 1 | 1 | 1 |
| 2  | vyzdvihnutie materiálu bez vlastnosti  | 0 | 1 | 0 | 0 |
| 3  | vyzdvihnutie materiálu s prioritnou vlastnosťou  | 0 | 0 | 1 | 0 |
| 4  | čas spracovania (normálneho) požiadavku do 1 minúty  | 0 | 1 | 1 | 1 |
| 5  | čas spracovania prioritného požiadavku do 1 minúty  | 0 | 0 | 1 | 1 |
| 6  | čas spracovania (normálneho) požiadavku nad 1 minútu  | 0 | 0 | 1 | 1 |
| 7  | čas spracovania prioritného požiadavku nad 1 minútu  | 0 | 0 | 0 | 1 |
| 8  | vytvorenie prioritnej požiadavky  | 0 | 0 | 1 | 1 |
| 9  | všetky sloty obsadene alebo prekročenie maximálnej váhy  | 0 | 0 | 1 | 0 |
| 10  | vozík je v režime iba_výklad  | 0 | 0 | 1 | 0 |
| 11  | vozík má voľný aspon jeden slot a po naložení materiálu nebude prekročená maximálna váha  | 1 | 1 | 1 | 0 |
| 12  | vozík ma naložený materiál s prioritnou vlastnosťou  | 0 | 0 | 1 | 0 |
| 70  | vyzdvihnutie (normálneho) materiálu  | false | true | false | false |
| 71  | vytvorenie prioritného požiadavku  | false | false | true | true |
| 72  | pridelenie materiálu prioritná vlastnosť  | false | false | true | true |
| 73  | vyzdvihnutie prioritného materiálu  | false | false | true | false |
| 74  | prepnutie do režimu iba_výklad  | false | false | true | true |
| 75  | vozík nenakladá material  | false | false | true | false |
| 76  | zotrvanie v režime iba_výklad  | false | false | true | false |
| 77  | prepnutie do výnimky  | false | false | false | true |

<hr>
<h2>Identifikácia vstupných parametrov testu:</h2>

| **Názov**  | **Popis**|
| :---: | :---: |
| `CountOfRequest`  | počet požiadavkov  |
| `CapacityOfCart`   | kapacita vozíka  |
| `SlotsOfCart` | počet slotov vozíka |
| `LengthOfTrack ` | dĺžka trasy |
| `CapacityFull ` | kapacita vozíka |
<hr>

<h2>Identifikácia charakteristiky parametrov + definícia ich blokov:</h2>

| **CountOfRequest**  | počet požiadavkov  |
| :---: | :---: |
| 1  | `CountOfRequest = 1`  |
| 2  | `CountOfRequest > 1`  |

 **CapacityOfCart**  | kapacita vozíka  |
| :---: | :---: |
| 1  | `CapacityOfCart = 50`  |
| 2  | `CapacityOfCart = 150`  |
| 3  | `CapacityOfCart = 500`  |

 **SlotsOfCart**  | počet slotov vozíka  |
| :---: | :---: |
| 1  | `SlotsOfCart = 1`  |
| 2  | `SlotsOfCart = 2`  |
| 3  | `SlotsOfCart = 3 or SlotsOfCart = 4`  |

 **LengthOfTrack**  | dĺžka trasy  |
| :---: | :---: |
| 1  | `LengthOfTrack < 60`  |
| 2  | `LengthOfTrack > 60 and LengthOfTrack < 120`  |
| 3  | `LengthOfTrack > 120`  |

| **CapacityCartFull**  | kapacita vozíka  |
| :---: | :---: |
| 1  | `CapacityCartFull = true`  |
| 2  | `CapacityCartFull = false`  |

| **SlotsCartFull**  | sloty vozíka  |
| :---: | :---: |
| 1  | `SlotsCartFull = true`  |
| 2  | `SlotsCartFull = false`  |

| **PrioritySet**  | nastavenie priority |
| :---: | :---: |
| 1  | `PrioritySet = true`  |
| 2  | `PrioritySet = false`  |

| **SUT constraints**  | podmienky  |
| :---: | :---: |
| 1  | `CapacityOfCart.1 -> !SlotsOfCart.1`  |
| 2  | `CapacityOfCart.3 -> SlotsOfCart.1 or SlotsOfCart.2`  |
| 3  | `PrioritySet.1 -> !LengthOfTrack.1`  |
| 4  | `CountOfRequest.2 and SlotsOfCart.1 -> SlotsCartFull.1`  |
| 5  | `!SlotsOfCart.1 and CountOfRequest.1 -> SlotsCartFull.2`  |
| 6  | `PrioritySet.1 -> LengthOfTrack.2`  |
| 7  | `!PrioritySet.1 -> LengthOfTrack.1`  |
| 8  | `PrioritySet.1 -> CapacityCartFull.1 or SlotsCartFull.1`  |
| 9  | `CountOfRequest.1 -> SlotsCartFull.2`  |
