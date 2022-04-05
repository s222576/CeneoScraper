# CeneoScraperAI

## Single opinion structure on [Ceneo.pl]()(https://www.ceneo.pl/)

|Element|Selector|Variable|
|-------|--------|--------|
|Opinion|div.js_product-review|opinion|
|Opinion id|\['data-entry-id'\]|opinion_id|
|Author|span.user-post__author-name|author|
|Recommendation|span.user-post__author-recomendation > em|rcmd|
|Stars score|span.user-post__score-count|score|
|Content|div.user-post__text|content|
|List of adventages|div.review-feature__title--positives ~ div.review-feature__item|pros|
|List of disadventages|div.review-feature__title--negatives ~ div. review-feature__item|cons|
|Date of posting opinion|span.user-post__published > time:nth-child(1)\['datetime'\]|posted_on|
|Date of purchasing product|span.user-post__published > time:nth-chil(2)\['datetime'\]|bought_on|
|For how many users useful|button.vote-yes > span|useful_for|
|For how many users useless|button.vote-no > span|useless_for|