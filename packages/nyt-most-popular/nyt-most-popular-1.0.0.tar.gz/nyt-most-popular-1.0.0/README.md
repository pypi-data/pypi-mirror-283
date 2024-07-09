# NytMostPopular Python SDK 1.0.0

Welcome to the NytMostPopular SDK documentation. This guide will help you get started with integrating and using the NytMostPopular SDK in your project.

## Versions

- API version: `2.0.0`
- SDK version: `1.0.0`

## About the API

Provides services for getting the most popular articles on NYTimes.com based on emails, shares, or views. Get most emailed articles for the last day: `/emailed/1.json` Get most shared articles on Facebook for the last day: `/shared/1/facebook.json` Get most viewed articles for the last seven days: `/viewed/7.json` ## Example Calls `https://api.nytimes.com/svc/mostpopular/v2/emailed/7.json?api-key=yourkey` `https://api.nytimes.com/svc/mostpopular/v2/shared/1/facebook.json?api-key=yourkey` `https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=yourkey`

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
pip install nyt-most-popular
```

## Services

The SDK provides various services to interact with the API.

<details> 
<summary>Below is a list of all available services with links to their detailed documentation:</summary>

| Name                                                               |
| :----------------------------------------------------------------- |
| [MostPopularService](documentation/services/MostPopularService.md) |

</details>
<br/>

## Models

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details> 
<summary>Below is a list of all available models with links to their detailed documentation:</summary>

| Name                                                                                                         | Description |
| :----------------------------------------------------------------------------------------------------------- | :---------- |
| [GetEmailedPeriodJsonOkResponse](documentation/models/GetEmailedPeriodJsonOkResponse.md)                     |             |
| [GetEmailedPeriodJsonPeriod](documentation/models/GetEmailedPeriodJsonPeriod.md)                             |             |
| [GetSharedPeriodJsonOkResponse](documentation/models/GetSharedPeriodJsonOkResponse.md)                       |             |
| [GetSharedPeriodJsonPeriod](documentation/models/GetSharedPeriodJsonPeriod.md)                               |             |
| [GetSharedByPeriodShareTypeJsonOkResponse](documentation/models/GetSharedByPeriodShareTypeJsonOkResponse.md) |             |
| [GetSharedByPeriodShareTypeJsonPeriod](documentation/models/GetSharedByPeriodShareTypeJsonPeriod.md)         |             |
| [ShareType](documentation/models/ShareType.md)                                                               |             |
| [GetViewedPeriodJsonOkResponse](documentation/models/GetViewedPeriodJsonOkResponse.md)                       |             |
| [GetViewedPeriodJsonPeriod](documentation/models/GetViewedPeriodJsonPeriod.md)                               |             |
| [EmailedArticle](documentation/models/EmailedArticle.md)                                                     |             |
| [Media](documentation/models/Media.md)                                                                       |             |
| [MediaMetadata](documentation/models/MediaMetadata.md)                                                       |             |
| [SharedArticle](documentation/models/SharedArticle.md)                                                       |             |
| [ViewedArticle](documentation/models/ViewedArticle.md)                                                       |             |

</details>
<br/>

## License

This SDK is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more details.
