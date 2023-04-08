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
| 1  | `CountOfReques = 1`  |
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
| 3  | `SlotsOfCart = 3`  |
| 4  | `SlotsOfCart = 4`  |

 **LengthOfTrack**  | dĺžka trasy  |
| :---: | :---: |
| 1  | `LengthOfTrack = 0`  |
| 2  | `LengthOfTrack = 1`  |
| 3  | `LengthOfTrack > 1`  |

| **CapacityFull**  | kapacita vozíka  |
| :---: | :---: |
| 1  | `CapacityFull = true`  |
| 2  | `CapacityFull = false`  |

| **SUT constraints**  | podmienky  |
| :---: | :---: |
| 1  | `CapacityOfCart.1 -> !SlotsOfCart.1`  |
| 2  | `CapacityOfCart.3 -> !SlotsOfCart.3 and !SlotsOfCart.4`  |
