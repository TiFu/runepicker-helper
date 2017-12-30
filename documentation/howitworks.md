title: Runepicker Helper - How it works
theme: sjaakvandenberg/cleaver-dark
output: howitworks.html

--

# Runepicker Helper

<div style="text-align:center; margin-top:100px; font-size:150%">
**We want to enable all players to quickly create, customize and select good 
rune pages based on automatically generated recommendations to improve the overall
quality of used rune pages.**
</div>

--

<div style="font-size: 200%; text-align:center"><b>Why?</b></div>


* Creating rune pages can be quite tedious - especially for low elo players
    * memorizing the effects of each rune is required to quickly create new pages while in champ select
* The current solution for many players is to copy the pages other players use
    * e.g. [probuilds.net](probuilds.net) 
    * This process takes relatively long: there might not be enough time to create the rune page in champ select

--

<div style="font-size: 200%; text-align:center"><b>Our Solution</b></div>

* User selects Champion and Role
* System generates a new rune page for the user and allows customization if required
    * includes a summary of the benefits of the generated rune page
* Allow user to create and select the rune page in LCU with 1 click (only available in the electron distribution)

<div style="font-size: 200%; text-align:center"><b>How?</b></div>

* Leverage machine learning to learn which rune pages perform well for a given champion
* Use the [LCU API](https://engineering.riotgames.com/news/architecture-league-client-update) to create and select the new rune page automatically

-- 

<div style="font-size: 200%; text-align:center"><b>Technical Details</b></div>

* Machine Learning
* Backend and Frontend
* LCU Integration

--

<div style="font-size: 200%; text-align:center"><b>Machine Learning - Overview</b></div>

* We used [tensorflow](https://www.tensorflow.org/) and [keras](https://keras.io/) to create 1 + 1 + 5 \* 4 + 5 \* 2 = 32 neural networks
    * Need 8 forward passes for each generated rune page 
* Built a generic framework
    * inputs, outputs and network architecture can be configured in [configuration files](https://github.com/TiFu/runepicker-helper/tree/master/ml/perks/netconfig)
    * enables fast iteration of network designs and easy adaption to new data inputs
* **95% Accuracy** for Top 2 Primary Style Prediction, **85% Accuracy** for Top 2 Sub Style Prediction
* Perks are hard to predict based on limited information in the API
    * e.g. there are no features indicating that 'Poro Ward' should be picked
    * **~ 50% Accuracy** on test data

-- 

<div style="font-size: 200%; text-align:center"><b>Machine Learning - Network Architecture</b></div>

* Very simple architecture with 2 - 3 layers
    * Inputs: champion id, role + tags (Fighter, Marksman, ...)
        * One Hot encoded
    * Outputs: predicted rune/style
    * see [configuration files](https://github.com/TiFu/runepicker-helper/tree/master/ml/perks/netconfig)
* Training takes about 2 minutes per network on a 3 year old laptop GPU
* Custom Metric to measure rune performance 
    * Target 1 if rune was picked and game **won**
    * Target 0 if rune was pickend and game **lost**
    * ignore otherwise
    * **Result:** network learns to predict if a user will win with a rune

--

<div style="font-size: 200%; text-align:center"><b>Machine Learning - Problems & Lessons Learnt</b></div>

* Classes need to be balanced: otherwise network learns to just predict one class/rune all the time
    * Oversampling or Undersampling
* Perk prediction is hard because the API does not provide good indicators for many perks (e.g. Poro Ward perk)
    * possible solution would be to gather behavioral stats about a player
        * e.g. dies to ganks very often, plays aggressive

--

<div style="font-size: 200%; text-align:center"><b>Backend & Frontend</b></div>

* Python backend for easy integration with keras
* [Socket.io](https://socket.io/) for communication between backend and frontend
* [Angular](https://angular.io/) for frontend


* (Preloaded) Models require 500 MB of RAM on the server
* small memory footprint for each request (selected champion, lane and primary style / sub style)
* Models can be evaluated in far less than one second on a CPU

--

<div style="font-size: 200%; text-align:center"><b>LCU Integration</b></div>

* **Enables Key Feature:** Inserting the generated rune page directly into the client with one click
    * only available in electron package
* LCU Client uses REST-API internally
    * can be leveraged to create and select the newly created rune page
    * Client automatically updates UI after changes
* shoutout to [Robert Manolea aka Pupix](https://github.com/Pupix) for his rift-explorer and lcu-connector package

--

<div style="font-size: 200%; text-align:center"><b>More Information</b></div>

* [Download our electron app](https://github.com/TiFu/runepicker-helper/releases)
* For more information and source code: [https://github.com/TiFu/runepicker-helper](https://github.com/TiFu/runepicker-helper)
    * Checkout the [documentation](https://github.com/TiFu/runepicker-helper/tree/master/documentation) 
      to get an overview of the folder structure
