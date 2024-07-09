# NytBooksSdk Python SDK 1.0.0

Welcome to the NytBooksSdk SDK documentation. This guide will help you get started with integrating and using the NytBooksSdk SDK in your project.

## Versions

- API version: `3.0.0`
- SDK version: `1.0.0`

## About the API

The Books API provides information about book reviews and The New York Times Best Sellers lists. 
### Best Sellers Lists Services 
#### List Names 
The lists/names service returns a list of all the NYT Best Sellers Lists. Some lists are published weekly and others monthly. The response includes when each list was first published and last published. `/lists/names.json` 
### List Data 
The lists/{date}/{name} service returns the books on the best sellers list for the specified date and list name. `/lists/2019-01-20/hardcover-fiction.json` Use current for {date} to get the latest list. `/lists/current/hardcover-fiction.json` 
### Book Reviews Services 
The book reviews service lets you get NYT book review by author, ISBN, or title. `/reviews.json?author=Michelle+Obama` `/reviews.json?isbn=9781524763138` `/reviews.json?title=Becoming`
Example Calls `https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=yourkey` `https://api.nytimes.com/svc/books/v3/reviews.json?author=Stephen+King&api-key=yourkey`

## Table of Contents

- [Setup & Configuration](#setup--configuration)
  - [Supported Language Versions](#supported-language-versions)
  - [Installation](#installation)
- [Services](#services)
- [Models](#models)
- [License](#license)

## Setup & Configuration

### Supported Language Versions

This SDK is compatible with the following versions: `Python >= 3.7`

### Installation

To get started with the SDK, we recommend installing using `pip`:

```bash
pip install nyt-books
```

## Services

The SDK provides various services to interact with the API.

<details> 
<summary>Below is a list of all available services with links to their detailed documentation:</summary>

| Name                                                               |
| :----------------------------------------------------------------- |
| [ListsJsonService](documentation/services/ListsJsonService.md)     |
| [ListsService](documentation/services/ListsService.md)             |
| [ReviewsJsonService](documentation/services/ReviewsJsonService.md) |

</details>

## Models

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details> 
<summary>Below is a list of all available models with links to their detailed documentation:</summary>

| Name                                                                                                                       | Description |
| :------------------------------------------------------------------------------------------------------------------------- | :---------- |
| [GetListsFormatOkResponse](documentation/models/GetListsFormatOkResponse.md)                                               |             |
| [GetListsDateListJsonOkResponse](documentation/models/GetListsDateListJsonOkResponse.md)                                   |             |
| [OverviewResponse](documentation/models/OverviewResponse.md)                                                               |             |
| [GetListsNamesFormatOkResponse](documentation/models/GetListsNamesFormatOkResponse.md)                                     |             |
| [GetListsBestSellersHistoryJsonOkResponse](documentation/models/GetListsBestSellersHistoryJsonOkResponse.md)               |             |
| [GetReviewsFormatOkResponse](documentation/models/GetReviewsFormatOkResponse.md)                                           |             |
| [GetListsFormatOkResponseResults](documentation/models/GetListsFormatOkResponseResults.md)                                 |             |
| [ResultsIsbns_1](documentation/models/ResultsIsbns1.md)                                                                    |             |
| [BookDetails](documentation/models/BookDetails.md)                                                                         |             |
| [ResultsReviews_1](documentation/models/ResultsReviews1.md)                                                                |             |
| [GetListsDateListJsonOkResponseResults](documentation/models/GetListsDateListJsonOkResponseResults.md)                     |             |
| [ResultsBooks](documentation/models/ResultsBooks.md)                                                                       |             |
| [BooksIsbns](documentation/models/BooksIsbns.md)                                                                           |             |
| [BooksBuyLinks_1](documentation/models/BooksBuyLinks1.md)                                                                  |             |
| [Result](documentation/models/Result.md)                                                                                   |             |
| [Lists](documentation/models/Lists.md)                                                                                     |             |
| [ListsBooks](documentation/models/ListsBooks.md)                                                                           |             |
| [BooksBuyLinks_2](documentation/models/BooksBuyLinks2.md)                                                                  |             |
| [GetListsNamesFormatOkResponseResults](documentation/models/GetListsNamesFormatOkResponseResults.md)                       |             |
| [Updated](documentation/models/Updated.md)                                                                                 |             |
| [GetListsBestSellersHistoryJsonOkResponseResults](documentation/models/GetListsBestSellersHistoryJsonOkResponseResults.md) |             |
| [ResultsIsbns_2](documentation/models/ResultsIsbns2.md)                                                                    |             |
| [RanksHistory](documentation/models/RanksHistory.md)                                                                       |             |
| [ResultsReviews_2](documentation/models/ResultsReviews2.md)                                                                |             |
| [GetReviewsFormatOkResponseResults](documentation/models/GetReviewsFormatOkResponseResults.md)                             |             |

</details>

## License

This SDK is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more details.

<!-- This file was generated by liblab | https://liblab.com/ -->
