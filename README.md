# Cross Probability Tool
Hello and welcome to my Women in Sports Data Hackathon project! 
My name is Caitlan and I am an undergraduate Engineering student at the University of Waterloo. I was so happy to be able to blend my curiosity in data science with my love of sports for this hackathon! I thank you in advance for reading and reviewing my submission. 

<br>
Please see the `Technical and build details` section at the bottom of this README for requirements and build details

## Purpose and Motivation
This project was inspired by the paper, [The quest for the right pass](http://statsbomb.com/wp-content/uploads/2021/11/Javier-M-Buldu.pdf) from the 2021 StatsBomb conference, and this paper, [Identifying Completed Pass Types and Improving Passing Lane Models](https://cs.uwaterloo.ca/~brecht/papers/passing-linhac-2022.pdf) from the Cheriton School of Computer Science. I decided to simplify scope and only look at cross passes for the purpose of this project. 

This tool was built to help coaching staff analyze and identify optimal cross locations based on their risk tolerance. The deployed app can be found at this link: https://caitlan-krasinski-crossing-probability-model-crossing-ui-41rlu3.streamlitapp.com

## Solution
This tool is contained in a simple UI for coaches to analyze historical cross events. 

The components of this tool is comprised of a classification model to predict the probability of a successful cross, a probability model to quantify the potential xG of a resultant cross and a simple optimization model. 

All exploratory analysis and model building can be found in the `notebooks` folder for further details on the models used for each component. 

**The optimization:** The objective function to identify the optimal cross is `MAX (xCross + (risk_tolerance-additional_risk_penalty) * xG)`

The risk tolerance is a way to assess the tradeoff between risk and reward. Since riskier crosses often reap greater rewards, I needed a way penalize high xG's that dominate the cross probabilty for when a coach values completed crosses and maintained possession over bold passes. The `additional_risk_penalty` is to further penalize xG as it has such extreme ranges. 

Various simplifications were made to the model. For instance, I only considered zones as cross destinations rather than individual teammate locations. This is becasue my understanding of crosses is that they are made to space rather than directly to foot. This may be an over simplification but the model can be extended in the future to look at specific teammate location. 
Another assumption is that the crosses are assumed to be made a height. Majority of historical crosses are made high in the air so this seemed like a reasonable assumtion to make. By making this assumption, it simplified the overall model as we did not need to account for the risk of interception anywhere between the origin zone and the destination zone or add the additional input of height. If we accounted for pass height, we would need differentiate the probability of interception from a ground level cross vs one high in the air that traverses over players rather than through.   
Additionally, the model only suggests a cross destination if there is support in that zone (ie: at least one teammate). This is naive in a way because players can run onto the ball but for simplicity empty zones are avoided. 

For the UI, the analysis is currently limited to historical events. Ideally I would have liked to build a UI where the user can place their team and opponenets on the plot and work out different scenarios, but given my limited app development experience this was not possibile for me in the time I had.
Each output shows the probability of a successful cross and the corresponding xG if that cross is a success. This model assumes that crosses are made to generate scoring chances, thus the reward in this model is xG. Since crosses are often made to space, the optimal *zone* is highlighted to identify which cross is ideal given the user's risk tolerance.
THe UI is a bit slow when flipping between cross events, runtime was not a priority in this project but in the future there can be ways to improve it. 


## Context
As mentioned, this tool was built to help coaching staff analyze and identify optimal cross locations based on their risk tolerance.

This tool could be used post game to analyze if crosses the team made were optimal to them and generated the best chance at scoring while still ensuring they are successful. 
If, as a coach, you prefer to make the sure bets to keep possesion, you may input your risk tolerance lower so that the optimization model knows you value completed crosses over potential high rewards. Conversely, if you are a risk-taker and value a potential high reward, you would input a higher risk tolerance.

## Difficulties and challenges
A major challenge I encountered was the limited data available for robust model training. I am still a novice when it comes to ML and finding ways to improve my models was a challenge. I think a main issue was that there are reletively few cross events in a game so there is less data to train on and cathc patterns for. This meant my cross probability model did not quite have the performance I desired but it was *good enough* for the proof of concept. 
Likewise, I had so few goal events that traning an xG model was challenging, given the lack of data and unbalanced nature in the classes, the model had an oversimplification issue where it more often than not, defaulted to classifying the shot as *no goal*. I couldn't find a way to finetune it in time so I resorted to using historical probabilities and using conditional probability to identify the probability of a goal from a specified zone, given the pressure in that zone (you can see further details in [this notebook](https://github.com/caitlan-krasinski/crossing-probability-model/blob/main/notebooks/xG_via_historical_prob.ipynb). 
Additionally, as mentioned earlier, I really wanted my model to come with a UI for interactive analysis. As a novice developer, the UI is quite simple and limited with what you can do with it, but luckily the `Streamlit` package made it possible. 
Lastly, the challenge of being a full time student also made it hard at times. I had high hopes for this project but time wasn't always on my side, that is why I found ways to simplify the project so I could get a completed project at the end of it. IN the end I am happy with my end solution and am proud of the work I put into it. 


## Technical and build details 
All work was done using Python and the UI was developed using Streamlit

Contents of the repo: 
- All exploratory analysis and model building can be found in the `notebooks` folder 
- UI code and supporting files are in the main directory of the repo in the `.py` files 
- Serialized models are in the `models` folder 

All necessary packages can be found in the requirements.txt file.

Nothing really needs to be built as you can just browse the web app or notebooks. All dev work was done in Jupyter notebooks, if you wish to run any of them you can launch a notebook server and run the code in there. 

If you did want to deploy the app locally, you can run `streamlit run crossing_ui.py` from the repo directory. 


<br>
Thank you for reading and reviewing my project! 
