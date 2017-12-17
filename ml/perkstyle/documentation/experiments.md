# Experiments: Primary Style Prediction

## 1: Simple

Input: tag1, tag2, role, 

Accuracy: ca. 74%

* bigger net: no improvement => model already extracted as much as possible from the input data
Suspect that not enough variables, because net learns, but bottoms out at high
error

## 2: Base Stats & CC

Input: tag1, tag2, \"role\", root, slow, stun, charm, knockup, base_ad, base_health, base_armor, base_mres, base_as, ad_scaling, health_scaling, armor_scaling, mres_scaling, as_scaling,

Accuracy: ca. 87%

## 3: cdPrimaryPerkstyle

Input: Additionally cd of abilities q, w, e, r early and late game

Improves detection of inspiration


## 4: Ability Scalign

Input: additionally input ad/ap/max_health/armor/mres scaling 

## Problem Tree: Inspiration

Training Data: 
             precision    recall  f1-score   support

          0       0.91      0.83      0.87      9986
          1       0.90      0.85      0.87     10070
          2       0.84      0.91      0.87     15565
          3       0.83      0.60      0.70      2458
          4       0.83      0.92      0.87      6921

avg / total       0.87      0.87      0.86     45000

Test data:
             precision    recall  f1-score   support

          0       0.91      0.85      0.88      1012
          1       0.90      0.86      0.88      1183
          2       0.83      0.90      0.86      1706
          3       0.81      0.54      0.65       294
          4       0.84      0.93      0.88       805

avg / total       0.86      0.86      0.86      5000

Inspiration has bad recall => we don't recognize many instances
of players choosing inspiration. 
Upon closer inspection of this tree, we noticed that only a small
subset of champions uses Inspiration. The two most common champs are
Ezreal and GP, both having an ability which applies on-hit effects. 

We first suspected that GP and Ezreal where not recognized by our neural net.
Running the prediction of our net only on games with Ezreal or GP revealed, that 
we indeed recognize these champions picking this tree with a recall of 99% and
\> 80% respectively. 

So why is our recall of instances of the inspiration tree so bad?
Well, we suspect there to be 

a) a high amount of noise caused by players not picking
the correct runes, not having updated their runes yet
b) our data does not model the reason for picking inspiration over another
   tree e.g. Sorcery for Malzahar (which more than 75% of the players picked)

b) illustrates one of the main problems with the inspiration tree.
   There's not an obvious benefit to picking this tree, which can be modelled
   by simple stats like AD or CD.