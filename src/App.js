import "./App.css";

function App() {
  return (
    <div className="App">
      <p className="page-title">Cramer Tweets</p>
      <TweetList data={tweets} />
    </div>
  );
}
export default App;

const tweets = await pullDB();
tweets.reverse();

async function pullDB() {
  try {
    const res = await fetch("http://localhost:3000/data");
    const tweets = await res.json();
    // console.log("Data fetched from the database:", tweets, typeof tweets);
    return tweets;
  } catch (E) {
    console.error(`pullDB Error ${E}`);
  }
}

function TweetList({ data }) {
  return (
    <div className="tweet-list-container">
      <ul className="tweet-list">
        {data.map((tweet) => (
          <li key={tweet.tweet_id} className="tweet-row">
            <p className="tweet-content">{tweet.content}</p>
            <p>
              <small>{tweet.companies}</small>
            </p>
            <small>{new Date(tweet.date).toLocaleString()}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
