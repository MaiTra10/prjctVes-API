# :gear: prjctVes-API
**prjctVes-API** is a REST API I developed to be used by [prjctVes](https://github.com/MaiTra10/prjctVes) to allow it to interact with a DynamoDB table and retrieve stock and CS:GO item price data. I created this REST API through the use of the AWS API Gateway and Lambda functions.

While this isn't meant to be a publicly available API as I only use it internally to send and receive data for the Discord bot (authorized via private API key), I will provide documentation for the different API Gateway resources.

## :electric_plug: Endpoints

**NOTE**: *These are only sample curl commands to show how the API is structured and will NOT return any data if executed*

POST &emsp;&ensp;```/prod/add```

<details>
  <summary>Example Request</summary>
  <p>
    <pre lang="">
curl -X POST https://sample-url.com/prod/add?for=stock&itemToAdd=TSLA:NASDAQ&user=USER_ID \
  -H 'x-api-key:API_KEY'
    </pre>
  </p>
</details>

<details>
  <summary>Example Response</summary>
  <p>
    <pre lang="python">
Status: 200
    </pre>
    OR
    <pre lang="python">
Status: 409
Body: 'Error: Duplicate Entry'
    </pre>
  </p>
</details>

GET &emsp;&emsp;```/prod/get```

<details>
  <summary>Example Request</summary>
  <p><br>
    Get all items in both watchlists
    <pre lang="">
curl https://sample-url.com/prod/get?for=both&user=USER_ID \
  -H 'x-api-key:API_KEY'
    </pre>
    Get all items from one of the two watchlists
    <pre lang="">
curl https://sample-url.com/prod/get?for=stock&user=USER_ID&retrieve=all \
  -H 'x-api-key:API_KEY'
    </pre>
    Get a specific item from one of the two watchlists
    <pre lang="">
curl https://sample-url.com/prod/get?for=stock&user=USER_IDretrieve=specific&index=1 \
  -H 'x-api-key:API_KEY'
    </pre>
  </p>
</details>

<details>
  <summary>Example Response</summary>
  <p><br>
    Get all items in both watchlists
    <pre lang="python">
Status: 200
Body: [{"item": "BNS:TSE", "userID": 305454779256012810, "ctx": ".s-2fe581d4-329d-4550-b245-49f832598737"},
      {"item": "AAPL:NASDAQ", "userID": 305454779256012810, "ctx": ".s-341d7ab5-65c3-4cf7-b2e3-5e8f3e780af5"},
      {"item": "TSLA:NASDAQ", "userID": 305454779256012810, "ctx": ".s-61c861bd-6cc2-4665-a1d7-b2a095e44adf"},
      {"item": "Horizon Case", "userID": 305454779256012810, "ctx": ".v-fe2fa2dd-1975-4564-9d0b-873e763b28f7"}]
    </pre>
    Get all items from one of the two watchlists
    <pre lang="python">
Status: 200
Body: [{"item": "BNS:TSE", "userID": 305454779256012810,"ctx": ".s-2fe581d4-329d-4550-b245-49f832598737"},
      {"item": "AAPL:NASDAQ", "userID": 305454779256012810, "ctx": ".s-341d7ab5-65c3-4cf7-b2e3-5e8f3e780af5"},
      {"item": "TSLA:NASDAQ", "userID": 305454779256012810, "ctx": ".s-61c861bd-6cc2-4665-a1d7-b2a095e44adf"}]
    </pre>
    Get a specific item from one of the two watchlists
    <pre lang="python">
Status: 200
Body: {"item": "BNS:TSE", "userID": 305454779256012810,"ctx": ".s-2fe581d4-329d-4550-b245-49f832598737"}
    </pre>
    OR
    <pre lang="python">
Status: 403
Body: 'Error: Table is empty'
    </pre>
    OR
    <pre lang="python">
Status: 400
Body: 'Error: Index is out of range. Only {count} entry/entries in watchlist!'
    </pre>
  </p>
</details>

DELETE &nbsp;&nbsp;```/prod/remove```

<details>
  <summary>Example Request</summary>
  <p>
    <pre lang="">
curl -X DELETE https://sample-url.com/prod/remove?for=stock&user=USER_ID&index=1 \
  -H 'x-api-key:API_KEY'
    </pre>
  </p>
</details>
<details>
  <summary>Example Response</summary>
  <p><br>
    Returns deleted entry
    <pre lang="python">
Status: 200
Body: {"item": "BNS:TSE", "userID": 305454779256012810, "ctx": ".s-2fe581d4-329d-4550-b245-49f832598737"}
    </pre>
    OR
    <pre lang="python">
Status: 403
Body: 'Error: Table is empty'
    </pre>
    OR
    <pre lang="python">
Status: 400
Body: 'Error: Index is Out of Range (1 - {count})'
    </pre>
  </p>
</details>

GET &emsp;&emsp;```/prod/steam```

<details>
  <summary>Example Request</summary>
  <p><br>
    Validate > to validate item name
    <pre lang="">
curl https://sample-url.com/prod/steam?requestType=validate&itemName=Horizon Case \
  -H 'x-api-key:API_KEY'
    </pre>
    Basic > to get basic price data
    <pre lang="">
curl https://sample-url.com/prod/steam?requestType=basic&itemName=Horizon Case \
  -H 'x-api-key:API_KEY'
    </pre>
    Advanced > to get basic price data plus a graph
    <pre lang="">
curl https://sample-url.com/prod/steam?requestType=advanced&itemName=Horizon Case \
  -H 'x-api-key:API_KEY'
    </pre>
  </p>
</details>

<details>
  <summary>Example Response</summary>
  <p><br>
    Validate
    <pre lang="python">
Status: 200
Body: Valid
    </pre>
    Basic
    <pre lang="python">
Status: 200
Body: {
      "success": true,
      "lowest_price": "CDN$ 1.24",
      "volume": "9,563",
      "median_price": "CDN$ 1.25"
      }
    </pre>
    Advanced
    <pre lang="python">
Status: 200
Body: {
      "success": true,
      "lowest_price": "CDN$ 1.24",
      "volume": "9,563",
      "median_price": "CDN$ 1.25",
      "prices": [["Jul 29 2023 01: +0", 1.288, "16240"], <- ... latest 750 data points ... ->, ["Sep 04 2023 05: +0", 1.248, "416"]],
      "historyAvailable": true,
      "imgURL": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUwnfbOdDgavYXukYTZkqf2ZbrTwmkE6scgj7CY94ml3FXl-ENkMW3wctOLMlhpVHKV9YA/360fx360f"
      }
    </pre>
    OR
    <pre lang="python">
Status: 404
Body: 'Error: Item not Found'
    </pre>
  </p>
</details>

GET &emsp;&emsp;```/prod/stock```

<details>
  <summary>Example Request</summary>
  <p><br>
    Validate > to validate item name
    <pre lang="">
curl https://sample-url.com/prod/stock?requestType=validate&ticker=AAPL&exchange=NASDAQ \
  -H 'x-api-key:API_KEY'
    </pre>
    Basic > to get basic price data
    <pre lang="">
curl https://sample-url.com/prod/stock?requestType=basic&ticker=AAPL&exchange=NASDAQ \
  -H 'x-api-key:API_KEY'
    </pre>
    Advanced > to get in depth price data
    <pre lang="">
curl https://sample-url.com/prod/stock?requestType=advanced&ticker=AAPL&exchange=NASDAQ \
  -H 'x-api-key:API_KEY'
    </pre>
  </p>
</details>
<details>
  <summary>Example Response</summary>
  <p><br>
    Validate
    <pre lang="python">
Status: 200
Body: Valid
    </pre>
    Basic
    <pre lang="python">
Status: 200
Body: {
      "Current Price": "$189.46",
      "% Change": 0.85
      }
    </pre>
    Advanced
    <pre lang="python">
Status: 200
Body: {
      "Current Price": "$189.46",
      "Previous Close": "$187.87",
      "Day Range": "$188.28 - $189.92",
      "Year Range": "$124.17 - $198.23",
      "Market Cap": "2.96T USD",
      "Average Volume": "55.35M",
      "P/E Ratio": "31.84",
      "Dividend Yield": "0.51%",
      "% Change": 0.85,
      "Name": "Apple Inc"
      }
    </pre>
    OR
    <pre lang="python">
Status: 404
Body: 'Error: Ticker or Exchange not Found'
    </pre>
  </p>
</details>
