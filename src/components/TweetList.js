import React from "react";
import "./TweetList.css";

function TweetList({ data }) {
  return (
    <div className="tweet-list-container">
      <ul className="tweet-list">
        {data.map((tweet) => (
          <li key={tweet.tweet_id} className="tweet-row">
            <p className="tweet-content">{tweet.content}</p>
            {tweet.companies && (
              <small className="companies">{tweet.companies}</small>
            )}
            <time>
              <small>
                {new Date(tweet.date).toLocaleTimeString("en-US", {
                  hour: "numeric",
                  minute: "numeric",
                }) + " • "}
              </small>
              <small>{new Date(tweet.date).toLocaleDateString()}</small>
            </time>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TweetList;
