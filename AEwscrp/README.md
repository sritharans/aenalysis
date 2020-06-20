# Welcome to the AE Listing Scrapper!

This is a simple tool written in F# using .Net Core 3.1.

## About
This is a web scraping tool to download an AliExpress item listing and extract similar listings to the item from other AliExpress merchants.
The output contains the description, URL and pricing of other similar listings.
The data could then be imported to perform price comparisons and other analysis.
This tool is dependent on the following 3rd party components:

 - [Puppeteer Sharp](https://www.puppeteersharp.com)
 - [F# Data](http://fsharp.github.io/FSharp.Data/)

# Build Instructions

> **Note:** You will require an Internet connection to build the program and run it. Web proxies are not supported, a direct Internet connection is required.

Steps:

 1. Download and install the .Net Core SDK v3.1 from [here.](https://dotnet.microsoft.com/download)
 2. Clone this Github repository or download it using **Clone or download > Download Zip** and extract it to your hard drive.
 3. Using the command line, switch to the cloned repository or extracted folder and run the following command:`dotnet restore`
 4. After a successful restore then run the following command: `dotnet build`
 5. Then finally run the program using: `dotnet run`
 6. Follow the instructions to generate the listing data using the program, like this:`dotnet run https://www.aliexpress.com/category/1511/watches.html 60 output.csv`

## To view the CSV

Open the generated CSV file in any text editor of your choice or compatible spreadsheet application.

### Authors

 - Sritharan Sivaguru
 - Mohamed Fathi Mohamed
