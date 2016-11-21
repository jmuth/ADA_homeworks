# Applied Machine Learning

Exercise 1 is split into two notebooks:
* **1_Analysis_and_Cleaning:**
    1. Check if `playerShort` is a unique key for the table (it is!)
    2. Remove the players without information on their skin color
    3. Merge rater1 and rater2 into a `skin_color` field
    4. Remove useless columns and columns containing info on referee (and not on players)
    5. Aggregate the table on `playerShort` following the rules:
        * **Keep only first value:** for values the we suppose to be unique for each player
        *  **Sum the values:** for cards, victories, ...
    6. Introduce a field `gravity` that take into account the IAT and Exp removed previously to wieght the cards received by the player.  