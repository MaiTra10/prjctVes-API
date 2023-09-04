# :gear: prjctVes-API
**prjctVes-API** is a REST API I developed to be used by [prjctVes](https://github.com/MaiTra10/prjctVes) to allow it to interact with its DynamoDB table and retrieve Steam Market and stock price data. I created this REST API through the use of the AWS API Gateway and Lambda functions.

While this isn't meant to be a publicly available API as I only use it internally to retrieve data for the Discord bot (authorized via private API key), I will provide documentation for the different API Gateway resources.

## :electric_plug: Endpoints

- POST &emsp;&ensp;```/prod/add```
<details>
  <summary>Example Request</summary>
  <p>
    <pre lang="python">curl -X POST https://4qq4mnhpug.execute-api.us-west-2.amazonaws.com/prod/add?for=stock&itemToAdd=TSLA:NASDAQ&user=USER_ID \
        -H 'x-api-key:API_KEY'
      </pre>
  </p>
</details>
<details>
  <summary>Example Response</summary>
  <p>
    <pre lang="python">Status: 400
    </pre>
  </p>
</details>

- GET &emsp;&emsp;```https://sample-url.com/prod/get```
- DELETE &nbsp;&nbsp;```https://sample-url.com/prod/remove```
- GET &emsp;&emsp;```https://sample-url.com/prod/steam```
- GET &emsp;&emsp;```https://sample-url.com/prod/stock```
