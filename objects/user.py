from text_sentiment import TextSentiment


class User:

    __slots__ = ["uid", "user_sentiment_list"]

    def __init__(self, uid, sentiment_data):

        user_sentiment_list = []
        for data in sentiment_data:
            text_sentiment_obj = TextSentiment(data['body'], data['sentiment_score'])
            user_sentiment_list.append(text_sentiment_obj)

        self.uid = uid
        self.user_sentiment_list = user_sentiment_list


