# Introduction
E-Commerce has become an important part of people's life. Many people use online market places such as Amazon, eBay, Lazada and Ali-Express to buy their items. There are many reasons why customers prefer this kind of shopping. Firstly, the wide range of product, secondly, the competition between sellers results in relatively low prices. Thirdly, it is easier to make online purchases. Lastly, it is more convenient to purchase online rather than to commute to the store. With the popularity of online shopping challenges have surfaced, customers have become used to this form of shopping, the platforms that hold these markets need to handle tons of data and sellers need to promote to their products differently. The need to build a tool that helps sellers to analyze the pricing of their products and compare their pricing with the other sellers’ pricing and help them to predict the rating of their products.

# The idea
The idea presented here is simple, sellers needs a place to help them make the right decision regarding their online store based on insights from the data that is available on their platform. Thus, the first step to build such as tool is to collect the data of the product. Next, this data needs to be cleaned and prepared. Then store the data in one place to be accessible. Then, a machine learning model needs to be selected and trained with the assistance of data. Lastly, to make a web application and mobile application to help the seller to access the information everywhere.

# The process

## Step One 
In this step the data have been collected using F# and Python from the Ali-Express web platform. The data categorized by the type and category (Watches, Computers, etc.), the collected data have many features such as min price, max price, name, URL, rating, seller name and so on. 

## Step two 
Store the data in a data store or database to be made available for preprocessing in the subsequent stages. Based on the volume of the data and many other features of the data, a No-SQL database was selected to be the main source of the data for our apps. There are many options like Hive, MongoDB and ArangoDB. ArangoDB has been selected to be the main database because it has a high integration level with Python and sufficient performance. Integration with Python will be uses later for the rest of the project.

## Step three
After storing the data in the database, in this step, the data needs to be collected and prepared to the upcoming steps. Here, the ArangoDB driver and Python language were used to complete this step, the data in this stage checked against many things such as missing values, its distribution, normalization, outliers and many other criteria.

## Step four 
This is the most important step where the analysis and modeling will be done. First the model needs to be selected. Then the selected model will be a regression algorithm because we need to predict a numeric value (Rating). The Random forest regression was selected and the model trained, built and tested.

## Step Five
This is the last step would be to materialize the whole idea. In this stage, the two interfaces are built (Web and mobile application).
