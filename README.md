# Retrieve raw events data

Your goal is to create a tool that gathers and parses events and related smart contracts information in
order to make them exploitable and create an API that can be used by the team.

#### Next : 
- Use case
  - Specifications
- Instructions
  - Programming language
  - Why do the coding exercise
  - Timeline to finish the exercise

## Use case

The data we manipulate in our application come from two different sources :

- a `csv file` completed by the events organizers
  that contains all the events information (for example, the event title, the event date, etc.)
- a `json file` containing the information of the new smart contract we deployed on the blockchain. The smart contract is associated with
  the event (using the event id) and contains the information related to the nft collection (ticket collection). 

In order to use these data and share them with our partners we would want them to be exposed via a REST API. The output that
we would expect for a given event should look like the example below :

```json
[
  {
    "eventId": 1,
    "title": "Mouse Party",
    "startDatetime": "2022-07-10T18:30:00",
    "endDatetime": "2022-07-11T01:00:00",
    "address": "1 Rue Alexandre Avisse 45000 Orléans",
    "locationName": "L'Astrolabe",
    "totalTicketsCount": 500,
    "assetUrl": "https://photos.com/mouseparty.png",
    "lineUp": [
      "Mehdi Maïzi",
      "Rad Cartier",
      "Squidji"
    ],
    "ticketCollections": [
      {
        "collectionName": "Mouse On",
        "scAddress": "KT1AKqxCJH9EPimNm1wo1BEgG9bFRgptJwkk",
        "collectionAddress": "KT1Apf8CPkYBe3bRuTCET6A4NhnosX2BAnp9",
        "pricePerToken": 4,
        "maxMintPerUser": 5,
        "saleSize": 500
      }
    ]
  }
]
```

### Specifications

- The fields name should be in camelCase not in snake_case.
- `lineUp` and `locationName` fields are optional. When the value doesn't exist, the field should be null. 
- `lineUp` field type is a list. In the csv file the different names are separated with "-".
- The format of the asset contained in the `assetUrl` field should be mp4 or png or jpeg. If it's not the case, the field should be null.
- The `scAddress` field corresponds to the "crowdsale" field in the input file `smart-contracts-data.json`. 
The `collectionName` field corresponds to the "collection" field in the input file.

## Instructions

We want a script that takes the two files contained in this repository (`organizers-data.csv` and `smart-contracts-data.json`)
as input and insert them into a database of your choice. Then, we want an API to expose these data. Here's a list of the different
use cases that we need:
- We want to be able to see a complete list of our events.
- We want to filter this list using the event sale start time.
- We want to be able to request a particular event using its id.
- We want to be able to update an event data (the event title, the line up, the image or video url and collection name)

We expect you to create and share with us a git repository with the code you produced. We should be able to launch and use the Api 
locally on all types of machine (MAC OS OR LINUX).

That means that we should easily be able to 
- start the DB 
- insert data 
- launch the API 
- trigger the API endpoints

### Programming Language

You can use any language (or framework/library) that you feel comfortable with to solve the problem.

### Why do the coding exercise?

We are a technology driven company and we have a passion for **clean code**.
Coding is a part of our day to day job and the role we offer is very hands-on.
We would like to make sure that anyone who joins us shares these values as well. So show us your passion for coding through this exercise!

### Timeline to finish the exercise

We appreciate you taking the time to do this exercise and as such there is a 7 days deadline for you to complete the assignment. 
Also, we don't want you to spend too much time in solving this exercise by creating very complex solution.
Be pragmatic and keep it simple like Uncle bob told us to... #KISS

