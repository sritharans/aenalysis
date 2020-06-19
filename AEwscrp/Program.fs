//////////////////////////////////////////////////////////////////////////////////////////////////////////
// About: This is a web scraping tool to download an AliExpress item listing and
//        extract similar listings to the item from other AliExpress merchants.
//        The output contains the description, URL and pricing of other similar listings.
//        The data could then be imported to perform price comparisons and other analysis.
//
// Authors: Sritharan Sivaguru (WQD180086)
//          Mohamed Fathi Mohamed (WQD180081)
//
// Learn more about F# at http://fsharp.org

open System

open canopy.types
open canopy.classic

open FSharp.Data
open FSharp.Text.RegexProvider

// CSV Schema that will be used for output later
type ItemInfo = CsvProvider<Sample = "Title,  PriceMin, PriceMax, Sold, Rating, Shipping, Store,  URL",
                            Schema = "string, float,    float,    int,  float,  float,    string, string",
                            HasHeaders = true>

type Ship = Regex<(@"Shipping: US \$(?<Ship>.*\.\d{2})")>
type Price = Regex<(@"^US \$(?<Price>.*\.\d{2})")>
type PriceRange = Regex<(@"^US \$(?<PriceMin>.*\.\d{2})\D*(?<PriceMax>.*\.\d{2})")>

let stripchar str = String.collect (fun c -> if (Char.IsNumber c || c = '.') then string c else "") str

let PriceMax price =
    let sprice = match price with
                 | pm when PriceRange().IsMatch (pm) -> PriceRange().TypedMatch(pm).PriceMax.Value
                 | pv when Price().IsMatch (pv) -> Price().TypedMatch(pv).Price.Value
                 | p -> p
    sprice |> stripchar |> float

let PriceMin price =
    let sprice = match price with
                 | pm when PriceRange().IsMatch (pm) -> PriceRange().TypedMatch(pm).PriceMin.Value                                          
                 | pv when Price().IsMatch (pv) -> Price().TypedMatch(pv).Price.Value
                 | p -> p
    sprice |> stripchar |> float

let Shipping price =
    let sprice = match price with
                 | s when Ship().IsMatch (s) -> Ship().TypedMatch(s).Ship.Value                                          
                 | _ -> "0.0"
    sprice |> stripchar |> float

let Sold (total :string) =
    stripchar total |> int

let eletext sel ele =
    match someElementWithin sel ele with
    | Some e -> e.Text
    | None -> "0"

let eleurl sel ele =
    let txt = (elementWithin sel ele).GetProperty("href")
    txt.Substring (0, txt.IndexOf ('?'))

[<EntryPoint>]
let main argv =
    match argv.Length with
    | 3 -> printfn "\n\tDownloading AliExpress listing data:"
           printfn "\t%s" argv.[0]
           
           start FirefoxHeadless
           resize (1280, 6485)
           url argv.[0]
           click "a.next-dialog-close"
           let df = [|for page in [1..(int argv.[1])] ->
                        if page > 1 && page < 60 then
                            click "button.next-btn.next-medium.next-btn-normal.next-pagination-item.next-next"
                            sleep 3
                        printfn "Parsing page: %i" page
                        js "window.scrollBy(0, document.body.scrollHeight);" |> ignore
                        let item = element "ul.list-items" |> elementsWithin "div.product-info"
                        [|for i in item -> 
                             (eletext ".item-title" i,
                              PriceMin (eletext ".price-current" i),
                              PriceMax (eletext ".price-current" i),
                              Sold (eletext ".sale-value-link" i),
                              eletext ".rating-value" i |> float,
                              Shipping (eletext ".shipping-value" i),
                              eletext ".store-name" i,
                              eleurl ".item-title" i)
                        |]
                    |] |> Array.concat
           quit ()

           use csv = new ItemInfo (Array.Parallel.map ItemInfo.Row df)
           csv.Save argv.[2]
           printfn "CSV Saved: %s, Rows: %d" argv.[2] df.Length

    | _ -> printfn "\tURL, range and CSV file name required."
           printfn "\tExample: dotnet run https://www.aliexpress.com/category/xxx/xxx.html 60 output.csv"
    0 // return an integer exit code
