# Applied Machine Learning


* **0 Analysis_and_Cleaning:**
    1. Check if `playerShort` is a unique key for the table (it is!)
    2. Remove the players without information on their skin color
    3. Merge rater1 and rater2 into a `skin_colour` field
    4. Remove useless columns and columns containing info on referee (and not on players)
    5. Aggregate the table on `playerShort` following the rules:
        * **Keep only first value:** for values the we suppose to be unique for each player
        *  **Sum the values:** for cards, victories, ...
    6. Introduce a field `gravity` that take into account the IAT and Exp removed previously to wieght the cards received by the player.  
    
* **1 Supervised Learning:**
    1. JONAS: fill it =P
    
* **2 Clustering:**
    1. Create a understandable matrix for a cluster algorithm (numerical values only)
    2. Run k-mean and computer silhouette and accuracy
    3. Iteratively remove the features increasing the most on of these scores, until we cannot do better
    4. Compare which features to keep to have max. silhouette or max. discrimination
