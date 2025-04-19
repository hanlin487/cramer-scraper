import React, { useState, useMemo, useEffect } from "react";
import "./TweetList.css";

function TweetList({ data }) {
  // the time range filter state set
  const [timeRange, setTimeRange] = useState(() => {
    return localStorage.getItem("timeRange") || "all";
  });

  // save the current range to localstorage and update whenever the range changes via user set
  useEffect(() => {
    localStorage.setItem("timeRange", timeRange);
  }, [timeRange]);

  const filteredData = useMemo(() => {
    const start = new Date();
    if (timeRange === "all") return data;

    const end = new Date();
    if (timeRange === "week") {
      end.setDate(start.getDate() - 7);
    } else if (timeRange === "month") {
      end.setMonth(start.getMonth() - 1);
    } else if (timeRange === "year") {
      end.setFullYear(start.getFullYear() - 1);
    }

    return data.filter((tweet) => new Date(tweet.date) >= end);
  }, [timeRange, data]);

  return (
    <div className="tweet-list-container">
      <div className="time-range-selector">
        <button
          className={timeRange === "all" ? "on" : ""}
          onClick={() => setTimeRange("all")}
        >
          All
        </button>
        <button
          className={timeRange === "week" ? "on" : ""}
          onClick={() => setTimeRange("week")}
        >
          Last Week
        </button>
        <button
          className={timeRange === "month" ? "on" : ""}
          onClick={() => setTimeRange("month")}
        >
          Last Month
        </button>
        <button
          className={timeRange === "year" ? "on" : ""}
          onClick={() => setTimeRange("year")}
        >
          Last Year
        </button>
      </div>
      <ul className="tweet-list">
        {filteredData.map((tweet) => (
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
