Analyze Textbook Index Terms
================

A term that appears in the index of a textbook has been selected by the
author & publisher as a subject to highlight. In this sense, a term in
the index is “important.”

# Setup

Load necessary packages and hard-code data locations. Note that the
data-loading chunks below assume you have run the textbook scraper
locally (i.e., that `masterlist.csv` is ready to go).

``` r
library(tidyverse)
```

    ## ── Attaching packages ─────────────────────────────────────── tidyverse 1.3.0 ──

    ## ✔ ggplot2 3.4.0     ✔ purrr   0.3.4
    ## ✔ tibble  3.1.2     ✔ dplyr   1.0.6
    ## ✔ tidyr   1.1.3     ✔ stringr 1.4.0
    ## ✔ readr   2.0.0     ✔ forcats 0.5.0

    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ## ✖ dplyr::filter() masks stats::filter()
    ## ✖ dplyr::lag()    masks stats::lag()

``` r
library(googlesheets4)
filename <- "../data_proc/masterlist.csv"
url_metadata <- "https://docs.google.com/spreadsheets/d/1n_fFptcgPIzzlNYHkUblP_cReWGNo3TKGJ-Bo7W5oA0/edit#gid=0"
```

Authenticate your Google account for Google Sheets access.

## Load metadata

Load the book metadata from our shared Google Sheet.

``` r
df_meta_raw <- read_sheet(
    url_metadata, col_types = str_c(c("cccc", rep("?", 20)), collapse = "")
  )
```

    ## ✔ Reading from "textbook-review".

    ## ✔ Range 'Included Textbooks'.

    ## New names:
    ## • `` -> `...22`
    ## • `` -> `...23`
    ## • `` -> `...24`

``` r
df_meta_raw %>% 
  glimpse()
```

    ## Rows: 1,004
    ## Columns: 24
    ## $ Author                   <chr> "<NA>", "Anderson", "Anderson, John D.", "Ang…
    ## $ Title                    <chr> "AISC Manual of Steel Construction: Allowable…
    ## $ `ISBN 13`                <chr> NA, "9781260471441", "9780078027673", "978047…
    ## $ Assigned                 <chr> "AJ", "KD", "ZDR", "AJ", "KD", "ZDR", "(ZDR)"…
    ## $ `PDF Stored`             <lgl> FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, TRUE, T…
    ## $ `OCR Needed`             <lgl> FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALS…
    ## $ Courselist               <lgl> FALSE, TRUE, FALSE, TRUE, TRUE, TRUE, TRUE, T…
    ## $ `Procured?`              <lgl> FALSE, TRUE, TRUE, FALSE, TRUE, TRUE, TRUE, T…
    ## $ `ILL Needed`             <lgl> FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, FALS…
    ## $ `No Index`               <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FAL…
    ## $ Inclusion                <chr> "Exclude", "Include", "Include", "Include", "…
    ## $ `ISBN 10`                <chr> "1564240002", "1260471446", "71238182", "0471…
    ## $ `Has Index?`             <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FAL…
    ## $ `On Knovel?`             <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FAL…
    ## $ `Courselist Institution` <lgl> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, N…
    ## $ Year                     <dbl> NA, 2020, NA, 2006, 2011, NA, NA, NA, 2015, N…
    ## $ Type                     <chr> NA, NA, "Foundation", NA, NA, NA, NA, NA, NA,…
    ## $ Discipline               <chr> "CEE", "Aero", "Aero", "CEE", "CEE", "ME", NA…
    ## $ `Known Courses`          <chr> "CE 426 (NCSU)", "Compressible Flows (UCLA)",…
    ## $ Link                     <chr> "XX - Interlibrary loan?", "https://icourse.c…
    ## $ Notes                    <chr> NA, "*3rd edition instead of 4th", NA, NA, NA…
    ## $ ...22                    <lgl> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, N…
    ## $ ...23                    <chr> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, N…
    ## $ ...24                    <dbl> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, N…

Process the metadata.

``` r
df_meta <- 
  df_meta_raw %>% 
  select(
    authors = Author,
    title = Title,
    ISBN = `ISBN 13`,
    courselist = Courselist,
    courselist_institution = `Courselist Institution`,
    need_ocr = `OCR Needed`,
    include = Inclusion,
    have_pdf = `PDF Stored`
  ) %>% 
  mutate(include = include == "Include") %>% 
  filter(!is.na(authors))
df_meta
```

    ## # A tibble: 103 x 8
    ##    authors  title    ISBN  courselist courselist_inst… need_ocr include have_pdf
    ##    <chr>    <chr>    <chr> <lgl>      <lgl>            <lgl>    <lgl>   <lgl>   
    ##  1 <NA>     AISC Ma… <NA>  FALSE      NA               FALSE    FALSE   FALSE   
    ##  2 Anderson Modern … 9781… TRUE       NA               TRUE     TRUE    TRUE    
    ##  3 Anderso… Introdu… 9780… FALSE      NA               FALSE    TRUE    TRUE    
    ##  4 Ang, Al… Probabi… 9780… TRUE       NA               FALSE    TRUE    FALSE   
    ##  5 Ashford… Technol… 9780… TRUE       NA               FALSE    TRUE    TRUE    
    ##  6 Beer     Vector … 9780… TRUE       NA               FALSE    TRUE    TRUE    
    ##  7 Bergman… Fundame… 9781… TRUE       NA               FALSE    TRUE    TRUE    
    ##  8 Bergman… Fundame… 9781… TRUE       NA               FALSE    TRUE    TRUE    
    ##  9 Bergstr… Mechani… 9780… FALSE      NA               FALSE    TRUE    TRUE    
    ## 10 Bevingt… Data re… 9780… TRUE       NA               TRUE     TRUE    TRUE    
    ## # … with 93 more rows

## Load scraped PDF data

This comes from the locally-stored `masterlist.csv` file.

``` r
df_raw <- read_csv(
  filename,
  col_types = "cc"
)
df_raw
```

    ## # A tibble: 64,750 x 2
    ##    Term                            ISBN         
    ##    <chr>                           <chr>        
    ##  1 "726 Index"                     9780521883030
    ##  2 "Virtual movement"              9780521883030
    ##  3 "see also"                      9780521883030
    ##  4 "virtual displacement"          9780521883030
    ##  5 "Virtual work"                  9780521883030
    ##  6 "x–xi"                          9780521883030
    ##  7 "for a rolling body"            9780521883030
    ##  8 "principle of"                  9780521883030
    ##  9 "in con\ue01eguration space"    9780521883030
    ## 10 "in terms of quasi-coordinates" 9780521883030
    ## # … with 64,740 more rows

## Process term data

Process the Index term data. “Atomize” the lines from each index into
single words. This will

``` r
df_data <- 
  df_raw %>% 
  rename(term = Term) %>% 
  # Atomize to single words
  # separate_rows(term) %>% 
  # Lowercase
  mutate(term = str_to_lower(term))

df_data
```

    ## # A tibble: 64,750 x 2
    ##    term                            ISBN         
    ##    <chr>                           <chr>        
    ##  1 "726 index"                     9780521883030
    ##  2 "virtual movement"              9780521883030
    ##  3 "see also"                      9780521883030
    ##  4 "virtual displacement"          9780521883030
    ##  5 "virtual work"                  9780521883030
    ##  6 "x–xi"                          9780521883030
    ##  7 "for a rolling body"            9780521883030
    ##  8 "principle of"                  9780521883030
    ##  9 "in con\ue01eguration space"    9780521883030
    ## 10 "in terms of quasi-coordinates" 9780521883030
    ## # … with 64,740 more rows

## Sanity-check available PDFs

Are any of the fully-digital PDFs unaccounted?

``` r
df_meta %>% 
  filter(include, have_pdf, !need_ocr) %>% 
  distinct(ISBN, .keep_all = TRUE) %>% 
  anti_join(df_data, by = "ISBN")
```

    ## # A tibble: 0 x 8
    ## # … with 8 variables: authors <chr>, title <chr>, ISBN <chr>, courselist <lgl>,
    ## #   courselist_institution <lgl>, need_ocr <lgl>, include <lgl>, have_pdf <lgl>

I’ve used the chunk above to track down “missing” PDFs; most of these
were due to ISBN’s that did not match between the PDF filename and the
metadata (Google) sheet.

## Need OCR

Which books do we need to run through OCR?

``` r
df_meta %>% 
  filter(include, have_pdf, need_ocr) %>% 
  select(authors, title)
```

    ## # A tibble: 11 x 2
    ##    authors                  title                                               
    ##    <chr>                    <chr>                                               
    ##  1 Anderson                 Modern compressible flow : with historical perspect…
    ##  2 Bevington, Philip R. an… Data reduction and error analysis for the physical …
    ##  3 Callen, Herbert B.       Thermodynamics and an introduction to thermostatist…
    ##  4 Craig                    Introduction to Robotics: Mechanics and Control     
    ##  5 Gurtin, Morton E.        The mechanics and thermodynamics of continua        
    ##  6 Hill, Terrell L.         An Introduction to Statistical Thermodynamics       
    ##  7 Kittel, Kroemer          Thermal Physics 2nd ed.                             
    ##  8 McQuarrie, Donald A.     Statistical mechanics                               
    ##  9 Sozen, Mete A            Understanding structures : an introduction to struc…
    ## 10 Speyer, Chung            Stochastic Processes, Estimation, and Control       
    ## 11 Strogatz, Steven Henry   Nonlinear dynamics and chaos: with applications to …

# Analyze

## Describe corpus

Count the number of book indexes in the corpus

``` r
df_data %>% 
  semi_join(
    .,
    df_meta %>% 
      filter(include),
    by = "ISBN"
  ) %>% 
  distinct(ISBN) %>% 
  count()
```

    ## # A tibble: 1 x 1
    ##       n
    ##   <int>
    ## 1    45

## Count terms

The following code detects the presence of certain keywords in the
textbook indexes. The `count` represents the number of textbooks whose
index includes the keyword, while the `frac` represents the fraction (of
our available corpus) that includes the keyword.

Note that some of the terms are multiply-defined; for instance,
`tradeoff` is counted if either `trade` or `tradeoff` is detected in the
Index.

``` r
# Define search terms
term_summaries <- list(
  "cost" = ~max(str_detect(.x, "cost")),
  "design" = ~max(str_detect(.x, "design")),
  "error" = ~max(str_detect(.x, "error")),
  "force" = ~max(str_detect(.x, "force")),
  "limit" = ~max(str_detect(.x, "limit")),
  "load" = ~max(str_detect(.x, "load")),
  "maximize" = ~max(str_detect(.x, "maximize|maximization")),
  "minimize" = ~max(str_detect(.x, "minimize|minimization")),
  "optimize" = ~max(str_detect(.x, "optimize|optimization")),
  "pressure" = ~max(str_detect(.x, "pressure")),
  "probability" = ~max(str_detect(.x, "probability")),
  "safety" = ~max(str_detect(.x, "safety")),
  "safety factor" = ~max(str_detect(.x, "safety factor|factor of safety")),
  "stress" = ~max(str_detect(.x, "stress")),
  "strength" = ~max(str_detect(.x, "strength")),
  "tolerance" = ~max(str_detect(.x, "tolerance")),
  "tradeoff" = ~max(str_detect(.x, "tradeoff|trade")),
  "uncertainty" = ~max(str_detect(.x, "uncertainty|uncertain")),
  "variability" = ~max(str_detect(.x, "variability")),
  "variation" = ~max(str_detect(.x, "variation"))
)

# Run analysis
df_counts <- 
  df_data %>% 
  semi_join(
    .,
    df_meta %>% 
      filter(include),
    by = "ISBN"
  ) %>% 
  group_by(ISBN) %>% 
  summarize(across(term, term_summaries)) %>% 
  summarize(
    across(-ISBN, sum),
    total = n()
  ) %>% 
  pivot_longer(
    cols = -total,
    names_to = "term",
    values_to = "count"
  ) %>% 
  mutate(
    term = str_remove_all(term, "term_"),
    frac = round(count / total, digits = 2)
  ) %>% 
  select(-total) %>% 
  arrange(desc(count)) 

df_counts %>% 
  knitr::kable()
```

| term          | count | frac |
|:--------------|------:|-----:|
| force         |    38 | 0.84 |
| pressure      |    34 | 0.76 |
| design        |    31 | 0.69 |
| limit         |    30 | 0.67 |
| stress        |    29 | 0.64 |
| load          |    24 | 0.53 |
| error         |    22 | 0.49 |
| strength      |    17 | 0.38 |
| variation     |    17 | 0.38 |
| probability   |    16 | 0.36 |
| safety        |    13 | 0.29 |
| cost          |    11 | 0.24 |
| optimize      |     9 | 0.20 |
| uncertainty   |     9 | 0.20 |
| safety factor |     6 | 0.13 |
| tradeoff      |     6 | 0.13 |
| variability   |     6 | 0.13 |
| tolerance     |     5 | 0.11 |
| minimize      |     2 | 0.04 |
| maximize      |     1 | 0.02 |

*Observations*

- Physics-related terms dominate the list; `force` is important in the
  vast majority of engineering textbooks.
- Uncertainty-related terms appear less frequently:
  - `probability` is important in 0.36 of textbooks. This is similar to
    `frac` of `strength`
  - `uncertainty` is important in 0.2 of textbooks. This is similar to
    `frac` of `optimize`
  - `tolerance` is important in 0.11 of textbooks. This is a very small
    fraction, but `tolerance` is quite a bit more specific than
    something like `uncertainty`
- “Error” shows up an intermediate number of times, but as EF has shown,
  the term has a highly-variable meaning to practicing engineers.
  - `error` is important in 0.49 of textbooks
