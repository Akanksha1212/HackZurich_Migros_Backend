## MigrosNudge Backend for HackZurich 2023


## Inspiration
**We all know from first-hand experience that sustaining an eco-friendly lifestyle can be challenging.**

When you're pressed for time, it's not always the first thing on your mind, and sometimes you might lack information on sustainable choices, or be deterred by higher costs. Our primary aim was to address these challenges and gently nudge users towards more sustainable products. We had several objectives in mind:

1) Increase awareness by clearly and conveniently showing users which products are sustainable and which are not while they shop.
2) Find innovative ways to encourage ALL customers(even students on a budget!) to adopt more sustainable practices.

## What it does

Our app is built to be integrated into the existing Migros app. One of the features we decided to augment is the **Scan, pay, done feature**. We've introduced a circular progress bar at the top of the screen which provides users with a sustainability score out of 100 and dynamically updates as they scan items. This score helps users gauge their sustainability efforts. Each user is assigned a personalised sustainability goal out of 100, determined through machine learning and mathematical modelling.  Additionally, we've incorporated a swap feature that leverages an AI-powered similarity model to suggest sustainable alternatives with a higher M-check score when a product is scanned. This way, the user can easily augment their score. We also have badges that users can unlock if they consistently score highly when they shop and meet the sustainability goals we set them. This could potentially be integrated into Cumulus rewards to provide cashback.

What sets our app apart is its dual purpose: not only does it raise awareness about your sustainability efforts right as you are shopping, but it also encourages you to aim for higher scores by incorporating gamification elements like the progress bar and achievable badges. Additionally, our machine learning model plays a crucial role in tailoring sustainability goals for each individual customer. This level of personalisation is especially significant because it accommodates lower-income customers, such as students, who may find sustainable swaps challenging due to their typically higher cost. Our model takes this financial constraint into consideration when determining the user's goal, ensuring that sustainability is accessible to everyone and enabling each user to contribute towards a more sustainable future.

## How we built it

Our goal-setting model factors in past goal achievement, average sustainability scores, and the user's spending habits. We categorize users into different groups based on their purchase history to determine if they are high, mid, or low-paying customers. Upon checkout, the user's next shopping goal is adjusted accordingly.  The front-end build is minimalistic and is made considering it'll be integrated at subitoGo feature of Migros app and it shows users their sustainability score and gamifies the process of sustainable shopping. 

## Challenges we ran into
We had a lot of challenges especially organizing work and different tech stacks posed a problem too but we were able to learn new things and we are happy that we got to work on Migros sustainable shopping challenge 

## Accomplishments that we're proud of
We are proud of building a working prototype in such a short time. 

## What we learned
We learned about teamwork, time management, and a lot more. Thanks to HackZurich for providing us with the platform to build our app

## What's next for MigrosApp
We designed our app to enhance the existing Migros app, so next the focus would be on seamlessly integrating the two for optimal functionality. For instance, user badges could potentially be transformed into Cumulus points. Moreover, our sustainable swap and sustainability scoring systems could enhance the shopping list feature, enabling users to prioritise sustainability in their future purchases. Finally, the goal-setting model should be trained on future customer data to determine the optimal goal score for a user’s grocery shop - this goal should strike a balance, being challenging enough to motivate the user to achieve it while simultaneously maximising their sustainability score.



