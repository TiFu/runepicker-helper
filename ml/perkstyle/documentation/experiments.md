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


