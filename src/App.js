import "./App.css";
import React from "react";
import TweetList from "./components/TweetList";
import useFetchTweets from "./hooks/useFetchTweets";

function App() {
  const { tweets, loading, error } = useFetchTweets();

  if (loading) {
    return <div>Loading tweets...</div>;
  }
  if (error) {
    return <div>Error loading tweets: {error}</div>;
  }

  return (
    <div className="App">
      <p className="page-title">Cramer Tweets</p>
      {tweets && <TweetList data={tweets} />}
    </div>
  );
}
export default App;
