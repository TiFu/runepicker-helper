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
    * inputs, outputs and network architecture configured in [configuration files](https://github.com/TiFu/runepicker-helper/tree/master/ml/perks/netconfig)
    * enables fast iteration of network designs and easy adaption to new data inputs
* **95% Accuracy** for Top 2 Primary Style Prediction
* Perks are difficult to predict based on limited information in the API
    * e.g. there are no features indicating that 'Poro Ward' should be picked

-- 

<div style="font-size: 200%; text-align:center"><b>Machine Learning - Network Architecture</b></div>

* Very simple architecture with 2 - 3 layers
    * Inputs: champion id, role + tags (Fighter, Marksman, ...)
    * Outputs: predicted rune/style
* Training takes about 2 minutes per network on a 3 year old laptop GPU
* Custom Metric to measure rune performance 
    * Target 1 / 0 if rune was picked and game **won** / **lost**
    * ignore otherwise
    * **Result:** network learns to predict if a user will win with a rune

--

<div style="font-size: 200%; text-align:center"><b>Machine Learning - Problems & Lessons Learnt</b></div>

* Classes need to be balanced: otherwise network learns to just predict one class/rune all the time
    * Oversampling or Undersampling
* Perk prediction is difficult because the API does not provide good indicators for many perks (e.g. Poro Ward perk)
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

* [Download our electron app](https://runehelper.heimerdinger.support/RunePicker%20Setup%201.0.0.exe)
* For more information and source code: [https://github.com/TiFu/runepicker-helper](https://github.com/TiFu/runepicker-helper)
    * Checkout the [README](https://github.com/TiFu/runepicker-helper/tree/master/) 
      to get an overview of the folder structure

[Go back to the main page](index.html)